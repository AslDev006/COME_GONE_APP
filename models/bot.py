import requests
from rest_framework import status
from rest_framework.response import Response
from .models import UserModel
from django.utils import timezone
from django.core.cache import cache
from decouple import config
BOT_TOKEN = config("BOT_TOKEN")
CHAT_ID = config("CHAT_ID")

def send_message_to_telegram(user):
    formatted_time = user.time.strftime("%d-%B %H:%M:%S")
    text = f"{'#Keldi' if user.status else '#Ketdi'}\n\n{user.user.full_name}\n{formatted_time}"
    
    response = requests.post(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        data={'chat_id': CHAT_ID, 'text': text}
    )
    print("Xabar muvaffaqiyatli yuborildi." if response.status_code == 200 else f"Xato: {response.status_code} - {response.text}")