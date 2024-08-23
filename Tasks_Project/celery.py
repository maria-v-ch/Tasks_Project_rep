from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from decouple import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tasks_Project.settings')

app = Celery('Tasks_Project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'check-comments-for-bad-words': {
        'task': 'tasks.tasks.check_comments_for_bad_words',
        'schedule': crontab(minute='*/10'),
    },
    'check-task-deadlines': {
        'task': 'tasks.tasks.check_task_deadlines',
        'schedule': crontab(hour=0, minute=0),
    },
}

app.conf.timezone = config('CELERY_TIMEZONE')
