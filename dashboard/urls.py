from django.urls import path
from .views import post_index, create_post, manage_user, create_user, manage_topic, create_topic, edit_post, delete_post, \
edit_user, delete_user, delete_topic, edit_topic

app_name = 'dashboard'

urlpatterns = [
    # for posts
  path('manage-post', post_index, name='post'),
  path('create-post', create_post, name='create-post'),
  path('edit/<str:slug>', edit_post, name='edit-post'),
  path('delete/<str:slug>', delete_post, name='post-delete'),

  # for users
  path('manage-user', manage_user, name='manage-user'), 
  path('create-user', create_user, name='create-user'), 
  path('ed/<int:pk>', edit_user, name='edit-user' ),
  path('del/<int:pk>', delete_user, name='user-delete' ),

  # for topic/categories
  path('manage-topic', manage_topic, name='manage-topic'), 
  path('create-topic', create_topic, name='create-topic'), 
  path('e/<slug:category_slug>', edit_topic, name='edit-topic'), 
  path('del/<slug:category_slug>', delete_topic, name='topic-delete'), 
]