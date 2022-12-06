import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
app = Celery('application')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
  'add-every-30-seconds': {
        'task': 'chats.tasks.send_no_read_message',
        'schedule': 30.0,
    },
}
app.conf.timezone = 'UTC'
