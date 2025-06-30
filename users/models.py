from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

import uuid
from datetime import timedelta

import random

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('caterer', 'Caterer'),
        ('driver', 'Delivery Driver'),
    )

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} Profile"
    
class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at
    
class MFADevice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    opt = models.CharField(max_length=6, blank=True, null=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def generate_otp(self):
        self.opt = str(random.randint(100000, 999999))
        self.expires_at = timezone.now() + timedelta(minutes=5)
        self.save()

    def is_valid(self, opt):
        return self.opt == opt and self.expires_at > timezone.now()