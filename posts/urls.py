from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_view, name='posts'),
    path('logout/', views.logout_view, name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('<int:post_id>/comments/', views.get_comments, name='get_comments'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
