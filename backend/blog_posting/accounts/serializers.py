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
        read_only=['id','author','created_at']

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
    likes_count= serializers.SerializerMethodField()
    liked_by_user= serializers.SerializerMethodField()


    def get_likes_count(self, obj):
        return Likes.objects.filter(post=obj).count()
    
    def get_liked_by_user(self,obj):
        request= self.context.get("request")
        if request and request.user.is_authenticated:
            return Likes.objects.filter(user= request.user, post=obj).exists()
        return False

 
    class Meta:
        model= BlogPost
        fields=['id','title','content','image','author',
                'created_at','updated_at','likes','comments','likes_count', 'liked_by_user']

    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['author'] = user  
        return super().create(validated_data)   