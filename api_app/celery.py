from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab

app = Celery('your_app')

app.conf.beat_schedule = {
    'send-daily-review-summary': {
        'task': 'your_app.tasks.send_daily_review_summary',
        'schedule': crontab(minute=0, hour=17),  # 5 PM every day
    },
}

app.conf.timezone = 'UTC'
