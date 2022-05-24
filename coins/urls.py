from django.urls import path
from rest_framework import routers
from .views import CoinTypeViewset, CoinViewset, update_coin

router = routers.DefaultRouter()
router.register(r'coin/type', CoinTypeViewset, basename='coin_type')
router.register(r'coins', CoinViewset, basename='coins')

urlpatterns = [
    path('update/coin/<coin_id>', update_coin, name="updated_product"),

] + router.urls
