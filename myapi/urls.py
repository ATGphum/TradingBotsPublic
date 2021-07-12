# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'BacktestResults2', views.BacktestResultsSetClass)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('BacktestResults/', views.BacktestResultsSet),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]