from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Review, EmailConfig, Recipient
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_daily_review_summary():
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    reviews = Review.objects.all()

    if not reviews.exists():
        return

    config = EmailConfig.objects.first() # Assuming only one config ever exists
    if config:
        send_time = config.send_time
        email_body = config.email_body
        smtp_server = config.smtp_server
        smtp_port = config.smtp_port
        smtp_username = config.smtp_username
        smtp_password = config.smtp_password

        recipients = Recipient.objects.all()
        recipient_emails = [recipient.email_address for recipient in recipients]

        # Set the SMTP backend details
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        settings.EMAIL_HOST = smtp_server
        settings.EMAIL_PORT = smtp_port
        settings.EMAIL_HOST_USER = smtp_username
        settings.EMAIL_HOST_PASSWORD = smtp_password
        settings.EMAIL_USE_TLS = True

        send_mail('Daily Review Summary', email_body, settings.DEFAULT_FROM_EMAIL, recipient_emails)
