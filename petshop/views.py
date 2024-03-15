from datetime import datetime
from django.shortcuts import render, redirect
from petshop.models import Category, Product, Cart, Order
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect



# Create your views here.
@login_required(login_url='/login')
def productlist(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'productlist.html',{'products':products, 'categories': categories})

def productdetail(request, p_id):
    categories = Category.objects.all()
    product = Product.objects.get(id=p_id)
    return render(request, 'productdetail.html',{'product':product, 'categories': categories})

def cartcreate(request, pdt_id):
    cart = Cart.objects.create(
        product = Product.objects.get(id=pdt_id),
        qty = request.GET.get('qty'),
        user_id = request.user.id,
    )
    cart.save()
    return redirect(f'/product/list/')

def cartlist(request):
    categories = Category.objects.all()
    cart = Cart.objects.filter(user_id=request.user.id)
    for item in cart:
        item.total = item.product.price * item.qty
    return render(request, 'cartlist.html',{'cart':cart, 'categories': categories})

def cartdelete(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect(f'/product/cartlist/')

def cartordercreate(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    product = []
    total = 0
    qty = 0
    for c in cart:
        product.append(c.product)
        qty = request.POST.get('qty')

    if qty is None:
        return HttpResponseRedirect('/product/cartlist/')

    try:
        qty = int(qty)
    except ValueError:
        return HttpResponseRedirect('/product/cartlist/')

    for c in cart:
        total += c.product.price * c.qty

    total *= qty

    total = c.product.price * int(qty)
    order = Order.objects.create(
        user_id = request.user.id,
        total_price = total,
        total_qty = qty,
        name = request.POST.get('name'),
        phone = request.POST.get('phone'),
        address = request.POST.get('address'),
        created_at=datetime.now()
    )
    order.product.set(product)
    cart.delete()
    return redirect(f'/product/list/')

def buynow(request,post_id):
    categories = Category.objects.all()
    product = Product.objects.get(id = post_id)
    if request.method == "GET":
        return render(request, 'ordercreate.html',{'product':product, 'categories': categories})
    elif request.method == "POST":
        qty = request.POST.get('qty')

        total = product.price * int(qty)
        order = Order.objects.create(
            product_id=product.id,
            user=request.user,
            total_qty=qty,
            total_price=total,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            created_at=datetime.now()
        )
        return redirect('/product/list')

def orderlist(request):
    categories = Category.objects.all()
    orders = Order.objects.filter(user_id = request.user.id)
    return render(request, 'orderlist.html',{'orders':orders, 'categories': categories})

def mylogin(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except Exception:
            messages.error(request, 'Email or Password is Incorrect!')
            return redirect('/login')
        else:
            if user.check_password(password):
                login(request, user)
                return redirect('/product/list/')
            else:
                messages.error(request, 'Email or Password is Incorrect!')
                return redirect('/login')
            
def mylogout(request):
    logout(request)
    return redirect('/login')

def userregister(request):
    if request.method == "GET":
        return render(request, 'register.html')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pw = request.POST.get('password')
        repw = request.POST.get('repassword')
        if pw == repw:
            if User.objects.filter( Q(username=username) | Q(email=email) ):
                messages.error(request, 'Username or Email already exit!')
                return redirect('/register')
            users = User.objects.create(
                username=username,
                email=email,
                password=make_password(pw)
            )
            login(request, users)
            return redirect('/product/list/')
        else:
            return redirect('/register/')


# For Admin
def list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'a_list.html',{'products':products, 'categories': categories})

def detail(request, p_id):
    categories = Category.objects.all()
    product = Product.objects.get(id=p_id)
    return render(request, 'a_detail.html',{'product':product, 'categories': categories})

def update(request, p_id):
    categories = Category.objects.all()
    if request.method == "GET":
        product = Product.objects.get(id=p_id)
        category = Category.objects.all()
        return render(request, 'update.html', {'product':product, 'category':category, 'categories': categories})
    if request.method == "POST":
        product = Product.objects.get(id=p_id)
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.qty = request.POST.get('qty')
        if request.FILES.get('image'):
            product.image.delete()
            product.image = request.FILES.get('image')
        product.category_id = request.POST.get('category')
        product.save()
        return redirect(f'/product/a_detail/{p_id}')
    
def delete(request, p_id):
    product = Product.objects.get(id=p_id)
    product.image.delete()
    product.delete()
    return redirect('/product/a_list/')

def create(request):
    categories = Category.objects.all()
    if request.method == "GET":
        category = Category.objects.all()
        return render(request, 'create.html',{'category':category, 'categories':categories})
    if request.method == "POST":
        category = Product.objects.create(
            image = request.FILES.get('image'),
            name = request.POST.get('name'),
            price = request.POST.get('price'),
            qty = request.POST.get('qty'),
            category_id = request.POST.get('category'),
        )
        return redirect('/product/a_list')
    
class OrderListView(ListView):
    model = Order
    template_name = 'a_order.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def admin_login(request):
    if request.method == "GET":
        return render(request, 'a_login.html')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'admin@gmail.com' and password == 'superuser':
            return redirect('/product/a_list/')
        else:
            messages.error(request, 'Email or Password is Incorrect!')
            return redirect('/admin_login')
        
def a_logout(request):
    logout(request)
    return redirect('/admin_login')


