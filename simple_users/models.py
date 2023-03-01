from django.db import models


class SimpleUser(models.Model):
    username = models.CharField(max_length=100, null=False, blank=False)
