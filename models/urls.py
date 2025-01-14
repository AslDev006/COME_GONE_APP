from django.urls import path
from .views import user_detail, pressed

urlpatterns = [
    path('user/', user_detail, name='user_detail'),  
    path('pressed/', pressed, name='pressed'),        
]