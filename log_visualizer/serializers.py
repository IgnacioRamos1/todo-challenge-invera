from rest_framework import serializers


class LogSerializer(serializers.Serializer):
    log = serializers.CharField()
