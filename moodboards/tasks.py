from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email, username):
    subject = f"Welcome, {username}!"
    message = f"Hello {username}, thanks for joining Moodboard Marketplace!"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

