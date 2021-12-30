from rest_framework import serializers


class IdSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255, required=True)