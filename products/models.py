from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_users.models import SimpleUser
from groups.models import Group


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)])
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(decimal_places=2, max_digits=10000, default=0)
    total = models.DecimalField(decimal_places=2, max_digits=10000, default=0, editable=False)

    owner = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, related_name="products")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)

    def calculate_total(self):
        return float(self.price * self.quantity)
