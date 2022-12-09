from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Task
from . import validators


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[
            validators.validate_title,
            ]
        )

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'expiration_date',
            'complete',
        ]
