from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "priority", "quantity", "price", "total", "owner", "group"]

    def get_total(self, obj):
        return obj.calculate_total()
