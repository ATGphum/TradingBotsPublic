from django.shortcuts import render

from rest_framework import viewsets

from .serializers import BacktestResultsSerializer
from .models import BacktestResults

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view 
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

# Create your views here

class BacktestResultsSetClass(viewsets.ModelViewSet):
    queryset = BacktestResults.objects.all()
    serializer_class = BacktestResultsSerializer

class BacktestResultsSet(APIView):
    def post(self, request, format=None):
        
        test = BacktestResults(fiat_balance=123, coin_balance=123, win_rate=41)
        serializer = BacktestResultsSerializer(test)
        return Response(serializer.data, status=status.HTTP_201_CREATED)