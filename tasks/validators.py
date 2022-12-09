from rest_framework import serializers


def validate_title(value):
    if not value:
        raise serializers.ValidationError(
            'Empty title is not allowed.'
            )
    elif len(value) >= 200:
        raise serializers.ValidationError(
            'Title is too long.'
            )
    return value
