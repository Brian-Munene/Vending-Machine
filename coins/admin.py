from django.contrib import admin
from .models import CoinType, Coins

admin.site.register(Coins)
admin.site.register(CoinType)
