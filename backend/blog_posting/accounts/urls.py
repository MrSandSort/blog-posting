from django.urls import path
from .views import RegisterView, BlogListCreateView, ProfileView, UserProfileAPIView

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
    path('user-profile/',UserProfileAPIView.as_view(), name='user-profile')
    
]