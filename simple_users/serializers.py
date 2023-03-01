from .models import SimpleUser
from rest_framework import serializers


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleUser
        fields = ["id", "username"]
