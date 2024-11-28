from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserModelSerializer, BlogPostSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from .models import BlogPost

class RegisterView(APIView):

    def get(self,request):
        blogs= User.objects.all()
        serializers=UserModelSerializer(blogs, many=True)
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

class LoginView(APIView):

    permission_classes= [AllowAny]

    def post(self,request):
        username= request.data.get('username')
        password= request.data.get('password')

        user= authenticate(username=username, password=password)

        if user is not None:
            token, created= Token.objects.get_or_create(user=user)
            return Response({'token':token.key}, status=status.HTTP_200_OK)
        
        return Response({'error':'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    

class BlogListCreateView(APIView):
    
    permission_classes=[IsAuthenticated]

    def get(self,request):
        blogs= BlogPost.objects.all().order_by('-created_at')
        serializers=BlogPostSerializer(blogs, many=True)
        return Response(serializers.data)
    
    def post(self,request):

        serializer = BlogPostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

