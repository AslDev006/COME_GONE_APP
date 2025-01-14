from celery import shared_task
from django.utils import timezone
from .models import UserModel

@shared_task
def update_user_status():
    today = timezone.now().date()
    users = UserModel.objects.all()
    
    for user in users:
        if user.time.date() == today:
            if (timezone.now() - user.time).total_seconds() < 86400:  
                continue

        user.status = not user.status
        user.time = timezone.now()  
        user.save()