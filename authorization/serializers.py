from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, max_length=32, required=True)


    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('User with this email already exists')
        return data

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['email'],password=validated_data['password'],email=validated_data['email'])
