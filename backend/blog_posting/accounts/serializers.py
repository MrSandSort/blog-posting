from rest_framework import serializers
from .models import UserProfile, Category, BlogPost, Comment, Likes
from django.contrib.auth.models import User
from django.utils.timesince import timesince


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        fields=['bio','profilePic']


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','username','email','password']

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
    # categories= serializers.SlugRelatedField(many=True, queryset=Category.objects.all(), slug_field='slug')
    comments= CommentSerializer(many=True, read_only=True)
    likes= LikeSerializer(many=True, read_only=True)
    time_since_posted=serializers.SerializerMethodField(); 

    def get_time_since_posted(self, obj):
        return timesince(obj.created_at)[0]

    class Meta:
        model= BlogPost
        fields=['id','title','content','image','author',
                'created_at','updated_at','likes','comments','time_since_posted']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the logged-in user
        validated_data['author'] = user  # Set the author to the logged-in user
        return super().create(validated_data)   