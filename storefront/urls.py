from django.urls import path
from storefront import views

app_name = 'storefront'

urlpatterns = [
    path('', views.index, name='index'),
    path('close_order/', views.close_order, name='close_order'),
    path('cart/', views.cart, name='cart'),
    path('orders_archive/', views.orders_archive, name='archive'),
    path('to_cart/<pk>', views.to_cart, name='to_cart'),

]
