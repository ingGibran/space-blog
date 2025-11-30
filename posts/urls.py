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
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('toggle_publish_post/<int:post_id>/', views.toggle_publish_post, name='toggle_publish_post'),
]
