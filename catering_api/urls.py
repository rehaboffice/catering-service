"""
URL configuration for catering_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView, RequestOTPView, VerifyEmailView, LogoutView, VerifyOTPView

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-email/', VerifyEmailView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

from users.views import RequestPasswordResetView, ResetPasswordView

urlpatterns += [
    path('request-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]

urlpatterns += [
    path('request-otp/', RequestOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
]

urlpatterns += [
    path('social/google/', GoogleLogin.as_view(), name='google_login'),
]

urlpatterns += [
    path('accounts/', include('allauth.urls')), 
    path('admin/', admin.site.urls),
    path('api/', include('menus.urls')),
    path('api/admin/analytics/', include('analytics.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('orders.urls')),

]
