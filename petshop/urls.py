from django.urls import path
from petshop.views import *

urlpatterns = [
    path('list/', productlist, name="productlist"),
    path('detail/<int:p_id>', productdetail, name="productdetail"),
    path('orderlist/', orderlist),
    path('buynow/<int:post_id>/', buynow),
    path('cartcreate/<int:pdt_id>/', cartcreate, name='cartcreate'),
    path('cartlist/', cartlist, name='cartlist'),
    path('cartdelete/<int:cart_id>/', cartdelete, name='cartdelete'),
    path('cartordercreate/', cartordercreate, name='cartordercreate'),

    path('create/', create, name="create"),
    path('a_list/', list, name="list"),
    path('a_detail/<int:p_id>/', detail, name="detail"),
    path('delete/<int:p_id>/', delete, name="delete"),
    path('update/<int:p_id>/', update, name="update"),
    path('order-list/', OrderListView.as_view(), name='order-list'),
]