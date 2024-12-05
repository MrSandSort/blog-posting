from django.urls import path
from .views import RegisterView, BlogListCreateView, ProfileView, UserProfileAPIView, BlogDetailView, UserBlogsAPIView, LikePostAPIView, CommentListCreateView, CommentDetailView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(), name='refresh'),
    path('blogs/',BlogListCreateView.as_view(), name='blog-list-create'),
    path('profile/',ProfileView.as_view(), name= 'profile-view'),
    path('user-profile/',UserProfileAPIView.as_view(), name='user-profile'),
    path('user-blogs/', UserBlogsAPIView.as_view(), name='user-blogs' ),
    path('my-blogs/<int:pk>/', BlogDetailView.as_view(), name='user-blog-detail'),
    path('blogs/<int:blog_id>/like/',LikePostAPIView.as_view(), name='like-posts'),
    path('blogs/<int:blog_id>/comments/', CommentListCreateView.as_view(), name='comments-list-create'),
    path('comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
]