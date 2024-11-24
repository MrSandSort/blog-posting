from rest_framework import serializers
from .models import UserProfile, Category, BlogPost, Comment, Likes
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        fields=['bio','profilePic']


class UserModelSerializer(serializers.ModelSerializer):
    profile= UserProfileSerializer(source='user-profile',read_only=True)

    class Meta:
        model= User
        fields=['id','username','email','profile']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields=['id','name','slug']

class CommentSerializer(serializers.ModelSerializer):
    author= serializers.StringRelatedField(read_only=True)
    post= serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Comment
        fields=['id','author','post','content','created_at']

class LikeSerializer(serializers.ModelSerializer):
    user= serializers.StringRelatedField(read_only=True)
    post= serializers.StringRelatedField(read_only=True)

    class Meta:
        model= Likes
        fields=['id','user','post','created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    categories= serializers.SlugRelatedField(many=True, queryset=Category.objects().all(), slug_field='slug')
    comments= CommentSerializer(many=True, read_only=True, source='comments')
    likes= LikeSerializer(many=True, read_only=True, source='likes')

    class Meta:
        model= BlogPost
        fields=['id','title','content','author','categories','image','status',
                'created_at','updated_at','likes','comments']