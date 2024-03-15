from django.contrib import admin
from petshop.models import Category, Product, Cart, Order

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'price', 'qty', 'category')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'qty')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'total_qty', 'total_price', 'name', 'phone', 'address', 'status', 'created_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)