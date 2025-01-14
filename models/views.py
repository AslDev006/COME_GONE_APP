import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserModel
from django.utils import timezone
from django.core.cache import cache
from .bot import send_message_to_telegram
@api_view(['GET', 'POST'])
def user_detail(request):
    if request.method == 'GET':
        users = UserModel.objects.all()
        data = [{"user": user.user, "status": user.status, "time": user.time} for user in users]
        return Response(data)

    elif request.method == 'POST':
        user_id = request.data.get('user')
        user_instance, created = UserModel.objects.get_or_create(user=user_id)
        return Response({"user": user_instance.user, "status": user_instance.status}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def pressed(request):
    user_id = request.data.get('user')
    user_instance = UserModel.objects.filter(user=user_id).first()

    if not user_instance:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    cache_key = f'pressed_{user_id}'
    
    if cache.get(cache_key) and (timezone.now() - cache.get(cache_key)).total_seconds() < 60:
        return Response({"error": "Bir daqiqa ichida yana so'rov yuborish mumkin emas."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    user_instance.status = not user_instance.status
    user_instance.time = timezone.now()
    user_instance.save()

    send_message_to_telegram(user_instance)

    cache.set(cache_key, timezone.now(), timeout=60)
    
    return Response({"message": "User updated successfully.", "status": user_instance.status}, status=status.HTTP_200_OK)