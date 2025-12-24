from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('register/', views.register, name='register'),
    path('create/', views.post_create, name='post_create'),
    path('edit/<int:post_id>/', views.post_edit, name='post_edit'),
]
