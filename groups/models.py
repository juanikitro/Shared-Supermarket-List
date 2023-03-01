from django.db import models
from simple_users.models import SimpleUser


class Group(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    estimated_total = models.DecimalField(decimal_places=2, max_digits=10000, default=0, editable=False)

    owner = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, related_name="groups")
    members = models.ManyToManyField(SimpleUser, related_name="groups_joined")
