from django.urls import path
from .views import PostList, PostDetail, CommentList

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:post_id>/comments/', CommentList.as_view(), name='comment_list'),

]