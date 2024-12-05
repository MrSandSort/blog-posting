from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import UserModelSerializer, BlogPostSerializer, UserProfileSerializer, LikeSerializer,CommentSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from .models import BlogPost, UserProfile, Likes, Comment

class RegisterView(APIView):

    def get(self,request):
        users= User.objects.all()
        serializers=UserModelSerializer(users, many=True)
        return Response(serializers.data)
    
    
    def post(self, request):

        serializer = UserModelSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.create_user(serializer.validated_data)

        return Response({"message": "User  created successfully"}, status=status.HTTP_201_CREATED)

    def create_user(self, validated_data):
        User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
    
class BlogListCreateView(APIView):
    

    permission_classes = [IsAuthenticated] 
    def get(self, request):
       
        blogs = BlogPost.objects.all().order_by('-created_at')
        serializer = BlogPostSerializer(blogs, many=True)
        return Response(serializer.data)

    
    def post(self,request):

        serializer = BlogPostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserModelSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        
        user = request.user
        data = request.data

        serializer = UserModelSerializer(user, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class UserProfileAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if UserProfile.objects.filter(user=request.user).exists():
            return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):

        try:
            profile = UserProfile.objects.get(user=request.user)
            profile.delete()
            return Response({"detail": "Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        

class UserBlogsAPIView(APIView):

    def get(self, request):
        blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
        serializer = BlogPostSerializer(blogs, many=True)
        return Response(serializer.data)
    

class BlogDetailView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            blog = BlogPost.objects.get(pk=pk)
            serializer = BlogPostSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
        serializer = BlogPostSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
        blog.delete()
        return Response({"message": "Blog deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id):
        try:
            post = BlogPost.objects.get(id=blog_id)
        except BlogPost.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        existing_like = Likes.objects.filter(user=request.user, post=post).first()

        if existing_like:
            existing_like.delete()
            liked_by_user = False
        else:
            Likes.objects.create(user=request.user, post=post)
            liked_by_user = True

        likes_count = Likes.objects.filter(post=post).count()

        return Response({
            "detail": "Post liked." if liked_by_user else "Post unliked.",
            "likes_count": likes_count,
            "liked_by_user": liked_by_user,
        }, status=status.HTTP_200_OK)
    
class CommentListCreateView(APIView):   
    permission_classes=  [IsAuthenticatedOrReadOnly]

    def get(self,request,blog_id):
        blogs= get_object_or_404(BlogPost, id= blog_id)
        comments = Comment.objects.filter(post=blogs)
        serializer= CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,blog_id):
        blogs= get_object_or_404(BlogPost, id=blog_id)
        serializer= CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author= request.user, post=blogs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDetailView(APIView):

    permission_classes=[IsAuthenticatedOrReadOnly]

    def get_object(self,comment_id):
        return get_object_or_404(Comment, id=comment_id)

    def get(self, request, comment_id):
        comment= self.get_object(comment_id)  
        serializer= CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, comment_id):
        comment = self.get_object(comment_id)
        if comment.author != request.user:
            return Response(
                {"detail": "You do not have permission to edit this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        if comment.author != request.user:
            return Response( {"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({"detail": "Comment deleted."}, status=status.HTTP_204_NO_CONTENT)