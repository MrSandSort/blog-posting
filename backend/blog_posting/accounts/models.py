
from django.db import models
from .models import Category
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    bio= models.TextField(blank=True, null= True)
    profilePic= models.ImageField(upload_to='profiles/', null=True)
    
    def __str__(self):
        return self.user.username
    
class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title= models.CharField(max_length=200)
    content= models.TextField()
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    status= models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='blog_posts')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Category(models.Model):
    name= models.CharField(max_length=100, unique=True)
    slug= models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post= models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    content= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    created_at= models.DateTimeField(auto_now_add=True)