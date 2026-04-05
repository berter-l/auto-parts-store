import os

from celery.schedules import crontab

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_parts_store.settings')


app = Celery('auto_parts_store')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.beat_schedule = {

    'delete_tokens': {
        'task': 'authentication.tasks.delete_tokens',
        'schedule': crontab(0, 0, day_of_month='2-30/2'),
        'args': (),
    }
}
