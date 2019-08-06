from django.urls import path
from storefront import views

app_name = 'storefront'

urlpatterns = [
    path('', views.index, name='index'),
    path('close_order/', views.close_order, name='close_order'),
    path('cart/', views.cart, name='cart'),
    path('orders_archive/', views.orders_archive, name='archive'),
    path('to_cart/<pk>', views.to_cart, name='to_cart'),
    path('new_book/', views.book_edit, name='new_book'),
    path('edit_book/<pk>', views.book_edit, name='edit_book'),
    path('show_users/', views.show_users, name='show_users'),
    path('show_books/', views.staff_book_list, name='show_books'),
    path('del_book/<pk>', views.del_book, name='del_book'),
    path('del_user/<pk>', views.del_user, name='del_user'),
    path('profile_book/<pk>', views.book_profile, name='profile_book'),
    path('by/<a_name>', views.index, name='by'),
    path('from/<g_name>', views.index, name='from'),

]
