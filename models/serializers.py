from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils import timezone
from django.db import transaction
from .models import UserModel, ComeGoneTimeModel

class UserModelSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(
        validators=[
            UniqueValidator(queryset=UserModel.objects.all(), message="Bu ID bilan foydalanuvchi allaqachon mavjud.")
        ]
    )

    class Meta:
        model = UserModel
        fields = ['user', 'full_name', 'status']

    def validate_user(self, value):
        if not (1 <= value <= 127):
            raise serializers.ValidationError("User ID 1 dan 127 gacha bo'lishi kerak.")
        return value

class ComeGoneTimeModelSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_id_display = serializers.IntegerField(source='user.user', read_only=True)
    user_updated_status = serializers.BooleanField(source='user.status', read_only=True)

    class Meta:
        model = ComeGoneTimeModel
        fields = [
            'id',
            'user',
            'user_id_display',
            'user_full_name',
            'status',
            'time',
            'user_updated_status'
        ]
        read_only_fields = ['id', 'status', 'time', 'user_id_display', 'user_full_name', 'user_updated_status']

    def create(self, validated_data):
        user_instance = validated_data['user']
        is_coming_event = not user_instance.status

        with transaction.atomic():
            come_gone_time_instance = ComeGoneTimeModel.objects.create(
                user=user_instance,
                status=is_coming_event,
                time=timezone.now()
            )
            user_instance.status = is_coming_event
            user_instance.save()
        return come_gone_time_instance