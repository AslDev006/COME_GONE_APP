import os
import shutil
from datetime import datetime
from celery import shared_task
from django.conf import settings
import time
from .bot import create_excel_report, send_excel_to_telegram
from .models import ComeGoneTimeModel    
@shared_task
def clear_media_folder():
    media_path = settings.MEDIA_ROOT

    if datetime.now().day == 6:
        for filename in os.listdir(media_path):
            file_path = os.path.join(media_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Faylni o'chirish
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Papkani o'chirish



@shared_task
def create_report_and_send(user_id):
    while True:
        file_path = create_excel_report(user_id)
        user = ComeGoneTimeModel.objects.get(user=user_id)  # User obyekti olish
        send_excel_to_telegram(user)
        time.sleep(120)  # 2 minut kutish