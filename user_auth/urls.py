from django.urls import path
from user_auth import views

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('login/', views, name='login'),
    # path('logout/', views, name='logout'),
    # path('edit_profile/<name>', views, name='edit'),
]
