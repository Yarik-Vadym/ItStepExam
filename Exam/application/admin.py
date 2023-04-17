from django.contrib import admin
from .models import Coins


@admin.register(Coins)
class CoinsAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'created_at', 'updated_at')

