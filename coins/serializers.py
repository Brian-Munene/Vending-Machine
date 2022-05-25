from rest_framework import serializers
from .models import Coins, CoinType, ProductPurchase, PurchaseCoins
from products.models import Product
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


class PurchaseCoinsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseCoins
        fields = '__all__'


class ProductPurchaseSerializer(serializers.ModelSerializer):
    purchase_coins = PurchaseCoinsSerializer(many=True)

    class Meta:
        model = ProductPurchase
        fields = '__all__'

    def validate(self, attrs):
        product = Product.objects.filter(id=attrs['product'].id).first()
        if not product:
            raise serializers.ValidationError({'product': 'Selected product does not exist'})

        if product.product_count < attrs['quantity']:
            raise serializers.ValidationError({"quantity": f'Product quantity is less than {attrs["quantity"]} '})

        return attrs

    def create(self):
        print('v', self.validated_data)
        purchase_instance = ProductPurchase.objects.create(**self.validated_data)
        purchase_instance.save()
        purchase_instance.refresh_from_db()
        return purchase_instance




