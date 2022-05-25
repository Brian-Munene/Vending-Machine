from django.urls import path
from rest_framework import routers
from .views import CoinTypeViewset, CoinViewset, update_coin, purchase_product

router = routers.DefaultRouter()
router.register(r'coin/type', CoinTypeViewset, basename='coin_type')
router.register(r'coins', CoinViewset, basename='coins')

urlpatterns = [
    path('update/coin/<coin_id>', update_coin, name="updated_product"),
    path('purchase/product', purchase_product, name="purchase_product"),

] + router.urls
