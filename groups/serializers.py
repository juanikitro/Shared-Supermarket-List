from .models import Group
from django.db import models
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    estimated_total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "priority", "quantity", "price", "estimated_total"]

    def get_estimated_total(self, obj):
        obj.estimated_total = float(Group.objects.filter(group=self).aggregate(models.Sum("total"))["total__sum"])
        return obj.estimated_total
