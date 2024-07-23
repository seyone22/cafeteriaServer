from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os

from api_app.models import EmailConfig

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafeteriaServer.settings')

app = Celery('api_app')


def get_email_config_schedule():
    config = EmailConfig.objects.first()
    if config:
        return crontab(hour=config.send_time.hour, minute=config.send_time.minute)
    return crontab(hour=0, minute=0)


app.conf.beat_schedule = {
    'send-daily-review-summary': {
        'task': 'api_app.tasks.send_daily_review_summary',
        'schedule': get_email_config_schedule(),
    },
}

app.conf.timezone = 'UTC'
