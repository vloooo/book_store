from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('books', views.BooksMetaView)
router.register('users', views.ShowUsers)

app_name = 'api'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.registration, name='sign_up'),
    path('edit_user/', views.profile_edit, name='edit_user'),
        # path('edit_book/', views.edit_book, name='edit_book'),

    path('to_cart/<int:pk>', views.to_cart, name='to_cart'),
    path('index/', views.index, name='index'),
    path('del_user/<int:pk>/', views.del_user, name='del_user'),
    path('close_order/', views.close_order, name='close_order'),

    # path('book/<pk>', views.api_book, name='api_book'),
    path('cart/', views.api_active_order, name='cart'),
    path('archive/', views.api_archive, name='archive'),
    path('user/', views.api_user, name='user'),
    path('', include(router.urls))
]
