from django.shortcuts import render

from rest_framework import viewsets

from .serializers import BacktestResultsSerializer
from .models import BacktestResults

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import datetime

# Create your views here

class BacktestResultsSetClass(viewsets.ModelViewSet):
    queryset = BacktestResults.objects.all()
    serializer_class = BacktestResultsSerializer


@csrf_exempt
def BacktestResultsSet(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
