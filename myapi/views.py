from django.shortcuts import render

from rest_framework import viewsets

from .serializers import BacktestResultsSerializer
from .models import BacktestResults

# Create your views here

class BacktestResultsSet(viewsets.ModelViewSet):
    queryset = BacktestResults.objects.all()
    serializer_class = BacktestResultsSerializer