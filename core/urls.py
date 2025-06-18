from django.urls import path
from .views import UserModelCreateAPIView, ComeGoneTimeModelCreateAPIView

urlpatterns = [
    path('scan/', UserModelCreateAPIView.as_view(), name='user-create'),
    path('user/', ComeGoneTimeModelCreateAPIView.as_view(), name='come-gone-time-create'),
]