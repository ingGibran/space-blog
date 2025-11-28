from django.urls import path
from .views import menu_view, menu_signup_view, menu_login_view

app_name = 'menu'

urlpatterns = [
    path('', menu_view, name='menu'),
    path('signup', menu_signup_view, name='menu_signup'),
    path('login', menu_login_view, name='menu_login'),
]