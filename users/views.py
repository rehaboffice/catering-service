from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializers, RequestOTPSerializer, RequestPasswordResetSerializer, ResetPasswordSerializer, VerifyOTPSerializer
from .models import EmailVerificationToken, User
from django.utils import timezone

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registered! Please verify yur email.'})
        return Response(serializer.errors, status=400)
    

class VerifyEmailView(APIView):
    def get(self, request):
        token_value = request.query_params.get('token')
        try:
            token = EmailVerificationToken.objects.get(token=token_value)
            if token.is_expired():
                return Response({'error': 'token expired.'}, status=400)
            token.user.is_active = True
            token.user.save()
            token.delete()
            return Response({'message': 'Email verified!'}, status=200)
        except EmailVerificationToken.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=400)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception:
            return Response({'error': 'Invalid token.'}, status=400)

class RequestPasswordResetView(APIView):
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset link sent!"})
        return Response(serializer.errors, status=400)
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful!"})
        return Response(serializer.errors, status=400)
    
class RequestOTPView(APIView):
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "OTP sent to your email"})
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP verified"})
        return Response(serializer.errors, status=400)
    