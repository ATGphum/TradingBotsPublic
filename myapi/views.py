from django.shortcuts import render

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

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

from backtesters.backtestrsi import backtest_rsi, backtest_rsi_external

# Create your views here

class BacktestResultsSetClass(viewsets.ModelViewSet):
    queryset = BacktestResults.objects.all()
    serializer_class = BacktestResultsSerializer

class BacktestResultsSet(APIView):
    def post(self, request, format=None):

        #result = backtest_rsi()
        result = backtest_rsi_external(request.data) #pass in json arguments
        resultmodel = BacktestResults(fiat_balance=result[0], coin_balance=result[1], win_rate=result[2])
        serializer = BacktestResultsSerializer(resultmodel)

        #if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)