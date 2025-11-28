from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_view, name='posts'),
]
