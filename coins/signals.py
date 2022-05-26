from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductPurchase, PurchaseCoins, Coins
from products.models import Product
import logging

logger = logging.getLogger('coins-logger')


@receiver(post_save, sender=ProductPurchase)
def update_product_count(sender, instance, created):
    """
     This function deducts the product count for the purchased product
    """
    if created:
        product = Product.objects.filter(id=instance.product.id).first()
        logger.info(f'Fetched the related product')
        if product:
            new_product_count = int(product.product_count) - int(instance.quantity)
            product.product_count = new_product_count
            product.save()
            logger.info(f'Updates product count to {product.product_count}')


@receiver(post_save, sender=PurchaseCoins)
def update_coin_count(sender, instance, created):
    """
    This function adds the coins that have been used in the purchase to the Coins.coin_count
    """
    if created:
        coin = Coins.objects.filter(coin_type=instance.coin_type).first()
        if coin:
            coin.coin_count = int(coin.coin_count) + int(instance.coin_count)
            coin.save()
