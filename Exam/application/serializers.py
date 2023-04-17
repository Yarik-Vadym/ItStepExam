from rest_framework import serializers
from .models import Coins


class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins
        fields = ('name', 'short_name', 'created_at', 'updated_at')