from rest_framework import serializers
from .models import Product, ProductType
import logging
from .utils import generate_slug

logger = logging.getLogger('products-logger')


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'price', 'product_count', 'product_type']
        extra_kwargs = {
            "name": {"required": True},
            'price': {'required': True},
            'product_count': {'required': True}
        }

    def validate(self, attrs):
        if attrs['product_count'] < 1:
            raise serializers.ValidationError({"product_count": "Product count cannot be less than 1."})
        return attrs

    def create(self):
        product = Product.objects.create(
            name=self.validated_data['name'],
            price=self.validated_data['price'],
            product_count=self.validated_data['product_count'],
            product_type=self.validated_data['product_type'],
        )
        product.save()

        logger.info(f'Product {product.id} has been saved to the database')
        product.refresh_from_db()

        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.product_count = validated_data.get('product_count', instance.product_count)
        instance.product_type = validated_data.get('product_type', instance.product_type)
        instance.save()
        instance.refresh_from_db()

        return instance


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
