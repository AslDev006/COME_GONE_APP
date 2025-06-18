from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserModelSerializer, ComeGoneTimeModelSerializer
from .bot import send_message_to_telegram
from .throttling import UserFieldRateThrottle # Yoki config.throttles dan

class UserModelCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserModelSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComeGoneTimeModelCreateAPIView(APIView):
    throttle_classes = [UserFieldRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = ComeGoneTimeModelSerializer(data=request.data)
        if serializer.is_valid():
            try:
                come_gone_instance = serializer.save()
                send_message_to_telegram(come_gone_instance)
                response_serializer = ComeGoneTimeModelSerializer(come_gone_instance)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"API XATOLIK: ComeGoneTimeModelCreateAPIView.post - {str(e)}")
                return Response(
                    {"error": "Serverda kutilmagan ichki xatolik yuz berdi.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)