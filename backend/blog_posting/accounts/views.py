from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserModelSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

class RegisterView(APIView):
    
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

    
 