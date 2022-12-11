from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, max_length=32, required=True)


    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('User with this email already exists')
        return data

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'],password=validated_data['password'],email=validated_data['username'])
