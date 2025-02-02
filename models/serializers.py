from rest_framework import serializers
from .models import UserModel, ComeGoneTimeModel

class UserModelSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    status = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return UserModel.objects.create(**validated_data)

class ComeGoneTimeModelSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    status = serializers.BooleanField(required=False)
    time = serializers.DateTimeField()

    def create(self, validated_data):
        return ComeGoneTimeModel.objects.create(**validated_data)