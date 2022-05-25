from django.db import models
from products.models import Product
import uuid


class CoinType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    value = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    slug = models.SlugField(max_length=200, unique=True)


class Coins(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    coin_type = models.ForeignKey(CoinType, related_name='coins', on_delete=models.PROTECT)
    coin_count = models.IntegerField(default=0, null=False, blank=False)


class ProductPurchase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=False, blank=False)
    quantity = models.IntegerField(default=0, null=False, blank=False)


class PurchaseCoins(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    coin_type = models.ForeignKey(CoinType, on_delete=models.PROTECT, related_name='purchase_coins')
    coin_count = models.IntegerField(default=0, null=False, blank=False)
    product_purchase = models.ForeignKey(ProductPurchase, on_delete=models.PROTECT, null=False, blank=False)

