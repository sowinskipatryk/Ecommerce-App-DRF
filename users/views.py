from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = get_object_or_404(CustomUser, username=username)

        if not user.check_password(password):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = CustomUserSerializer(user)

        return Response({'user': serializer.data, 'token': token.key})


class SignupView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            username = request.data.get('username')
            password = request.data.get('password')
            role = request.data.get('role')

            user = CustomUser.objects.get(username=username)
            user.set_password(password)

            if role == 'client':
                user.is_client = True
            elif role == 'seller':
                user.is_seller = True
            
            user.save()
            token = Token.objects.create(user=user)

            return Response({'user': serializer.data, 'token': token.key})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
