from rest_framework import serializers
from .models import User
from django.utils import timezone
from .models import EmailVerificationToken
import uuid

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