from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import BasePermission

class IsCaterer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'caterer'