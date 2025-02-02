from django.urls import path
from .views import UserModelCreateAPIView, ComeGoneTimeModelCreateAPIView

urlpatterns = [
    path('user/', UserModelCreateAPIView.as_view(), name='user-create'),
    path('procces/', ComeGoneTimeModelCreateAPIView.as_view(), name='come-gone-time-create'),
]