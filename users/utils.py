from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email, token):
    subject = 'Verify Your Email'
    message = f'Please click on the link to verify your email: http://127.0.0.1:8000/api/auth/verify-email/?token={token}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

def send_password_reset_email(email, token):
    subject = 'Reset Your Password'
    message = f'Please click on the link to reset your password: \nhttp://127.0.0.1:8000/api/auth/reset-password/?token={token}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])