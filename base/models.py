from django.db import models


class Message(models.Model):
    wifi = models.CharField(max_length=255, null=True, blank=True)
