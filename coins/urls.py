from django.urls import path
from rest_framework import routers
from .views import CoinTypeViewset

router = routers.DefaultRouter()
router.register(r'coin/type', CoinTypeViewset, basename='coin_type')

urlpatterns = [

] + router.urls
