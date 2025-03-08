from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from base.models import User
from base.serializers import UserRegistrationSerializer, UserSerializer
from base.permissions import IsAdminUser
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
import time

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'role': user.role
                    }
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
@method_decorator(vary_on_cookie, name='dispatch')
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        cache_key = 'all_users'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        queryset = User.objects.all()
        cache.set(cache_key, queryset, timeout=60 * 15)  # Cache for 15 minutes
        return queryset