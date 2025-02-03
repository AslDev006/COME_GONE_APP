from django.conf import settings
import os
import requests
from .models import ComeGoneTimeModel
from rest_framework import status
from .models import UserModel
from django.utils import timezone
from django.core.cache import cache
from decouple import config
import pandas as pd
from decouple import config


BOT_TOKEN = config("BOT_TOKEN")
CHAT_ID = config("CHAT_ID")


def create_excel_report(user_id):
    data = ComeGoneTimeModel.objects.filter(user_id=user_id).values()
    df = pd.DataFrame(data)

    # Excel faylni saqlash
    file_path = os.path.join(settings.MEDIA_ROOT, f'{user_id}_come_gone_time_report.xlsx')
    df.to_excel(file_path, index=False)
    
    return file_path


def send_message_to_telegram(user):
    formatted_time = user.time.strftime("%d-%B %H:%M:%S")
    text = f"{'#Keldi' if user.status else '#Ketdi'}\n\n{user.user.full_name}\n{formatted_time}"
    
    response = requests.post(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        data={'chat_id': CHAT_ID, 'text': text}
    )
    print("Xabar muvaffaqiyatli yuborildi." if response.status_code == 200 else f"Xato: {response.status_code} - {response.text}")




def send_excel_to_telegram(file_path):
    with open(file_path, 'rb') as file:
        response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument',
            data={'chat_id': CHAT_ID},
            files={'document': file}
        )
    print("Excel fayli muvaffaqiyatli yuborildi." if response.status_code == 200 else f"Xato: {response.status_code} - {response.text}")