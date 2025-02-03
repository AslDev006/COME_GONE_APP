from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # O'z loyihangiz nomini yozing
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True

# Har 24 soatda vazifani rejalashtirish
from celery.schedules import crontab

app.conf.beat_schedule = {
    'clear-media-folder-every-month': {
        'task': 'your_app.tasks.clear_media_folder',
        'schedule': crontab(hour=0, minute=0, day_of_month='6'),  
    },
}