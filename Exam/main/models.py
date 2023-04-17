from django.db import models
from django.urls import reverse


class FilterModel(models.Model):
    name_coin = models.CharField(verbose_name='NameCoin', max_length=10)
    choice_status = models.CharField(verbose_name='Select', max_length=15)
