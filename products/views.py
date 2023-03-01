from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from simple_users.decorators import login_simulation_required
from django.utils.decorators import method_decorator


@method_decorator(login_simulation_required, name="dispatch")
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("-priority")
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def performe_update(self, serializer):
        serializer.save()


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def performe_destroy(self, serializer):
        instance = serializer.save()
        instance.delete()
