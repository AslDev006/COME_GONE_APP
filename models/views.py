from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel, ComeGoneTimeModel
from .serializers import UserModelSerializer, ComeGoneTimeModelSerializer
from datetime import datetime
from .bot import send_message_to_telegram

class UserModelCreateAPIView(APIView):
    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserModelSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComeGoneTimeModelCreateAPIView(APIView):
    def post(self, request):
        request.data['time'] = datetime.now()
        serializer = ComeGoneTimeModelSerializer(data=request.data)
        if serializer.is_valid():
            come_gone_time = serializer.save()
            user = come_gone_time.user
            come_gone_time.status = user.status
            user.status = not user.status
            come_gone_time.save()
            user.save()  
            send_message_to_telegram(come_gone_time)
            return Response(ComeGoneTimeModelSerializer(come_gone_time).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)