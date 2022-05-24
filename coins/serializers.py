from rest_framework import serializers
from .models import Coins, CoinType
import logging

logger = logging.getLogger('coins-logger')


class CoinTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoinType
        fields = '__all__'


class CoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coins
        fields = '__all__'

    def validate(self, attrs):
        if attrs['coin_count'] < 1:
            raise serializers.ValidationError({"coin_count": "Coin count cannot be less than 1."})
        return attrs

    def update(self, instance, validated_data):
        instance.coin_type = validated_data.get('coin_type', instance.coin_type)
        instance.coin_count = validated_data.get('coin_count', instance.coin_count)
        instance.save()
        instance.refresh_from_db()

        return instance

