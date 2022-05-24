from rest_framework import serializers
from .models import Coins, CoinType
import logging

logger = logging.getLogger('coins-logger')


class CoinTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoinType
        fields = '__all__'
