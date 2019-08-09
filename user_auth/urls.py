from django.urls import path
from user_auth import views
from django.contrib.auth.views import LogoutView

app_name = 'auth'
urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='auth:login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.profile_edit_view, name='edit'),
]
