from django.urls import path
from rest_framework import routers
from .views import CoinTypeViewset, CoinViewset

router = routers.DefaultRouter()
router.register(r'coin/type', CoinTypeViewset, basename='coin_type')
router.register(r'coins', CoinViewset, basename='coins')

urlpatterns = [

] + router.urls
