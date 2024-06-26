from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Review
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_daily_review_summary():
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    reviews = Review.objects.filter(created_at__date=today)

    if not reviews.exists():
        return

    subject = f'Daily Review Summary for {today}'
    message = 'Here are the reviews for the day:\n\n'

    for review in reviews:
        message += f'- {review.content}\n'  # Adjust based on your model fields

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['recipient@example.com'])
