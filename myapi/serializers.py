# serializers.py
from rest_framework import serializers

from .models import BacktestResults

class BacktestResultsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BacktestResults
        fields = ('fiat_balance', 'coin_balance', 'win_rate')