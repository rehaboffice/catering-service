from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'full_name', 'role', 'is_staff']
    search_fields = ['email', 'full_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name', 'role', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Profile)