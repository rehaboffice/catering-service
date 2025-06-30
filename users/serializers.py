from rest_framework import serializers
from .models import User, PasswordResetToken
from django.utils import timezone
from .models import EmailVerificationToken, MFADevice
import uuid
from .utils import send_password_reset_email
from django.core.mail import send_mail
from django.conf import settings

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()

        token = EmailVerificationToken.objects.create(user=user)

        from .utils import send_verification_email
        send_verification_email(user.email, token.token)

        return user
    
class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return email
    
    def save(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)

        token = PasswordResetToken.objects.create(user=user)
        send_password_reset_email(user.email, str(token.token))

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only = True, min_length = 8)

    def validate(self, data):
        try:
            token_obj = PasswordResetToken.objects.get(token=data['token'])

        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid token."}) 
        
        if token_obj.is_expired():
            raise serializers.ValidationError({"token": "Token has expired."})
        
        data['user'] = token_obj.user
        return data
    
    def save(self):
        user = self.validated_data['user']
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()

        PasswordResetToken.objects.filter(user=user).delete()

class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User not found.")
        return email
    
    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        mfa, _ = MFADevice.objects.get_or_create(user=user)
        mfa.generate_otp()
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is {mfa.otp}.",
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            mfa = MFADevice.objects.get(user=user)
        except:
            raise serializers.ValidationError("Invalid email or OTP")

        if not mfa.is_valid(data['otp']):
            raise serializers.ValidationError("Invalid or expired OTP")

        return data