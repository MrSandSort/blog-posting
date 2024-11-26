from django.urls import path
from .views import RegisterView,LoginView, BlogListCreateView

urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('blogs/',BlogListCreateView.as_view(), name='blog-list-create')
]