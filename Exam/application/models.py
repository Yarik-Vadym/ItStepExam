from django.db import models


class Coins(models.Model):
    coins_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)