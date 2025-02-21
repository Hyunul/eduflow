from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from common.logger import log_event
from users.signals import get_client_ip
from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from common.permissions import IsSelfOrAdmin

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            log_event(f'✅ JWT 로그인 성공: {request.data.get("username")} | IP: {get_client_ip(request)}')
        else:
            log_event(f'❌ JWT 로그인 실패: {request.data.get("username")} | IP: {get_client_ip(request)}', level='warning')
        return response
    
class RegisterView(APIView):
    permission_classes = [~IsAuthenticated]  # 비로그인 상태에서만 접근 가능
    
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': '회원가입 성공'
        }, status=status.HTTP_201_CREATED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # 관리자만 전체 사용자 관리
    
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsSelfOrAdmin()]
        return super().get_permissions()