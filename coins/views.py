from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import CoinTypeSerializer, CoinSerializer, ProductPurchaseSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging

from .models import CoinType, Coins
from products.models import Product
from .utils import *

logger = logging.getLogger('coins-logger')


class CoinTypeViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = CoinType.objects.all()
    serializer_class = CoinTypeSerializer

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['update', 'partial_update', 'destroy', 'list', 'create']:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()


class CoinViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Coins.objects.all()
    serializer_class = CoinSerializer

    def get_permissions(self):
        """Set custom permissions for each action."""
        if self.action in ['update', 'partial_update', 'destroy', 'list', 'create', 'put']:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_coin(request, coin_id):
    if request.user.is_staff:
        coin = Coins.objects.filter(coin_type=coin_id).first()
        if not coin:
            return Response({
                'message': 'Coin was not found'
            }, status=status.HTTP_404_NOT_FOUND)

        coin_serializer = CoinSerializer(instance=coin, data=request.data)
        if coin_serializer.is_valid():
            _product = coin_serializer.save()
            response = Response()
            response.data = {
                'user':    CoinSerializer(coin).data,
                'success': 'Coin updated successfully'
            }
            return response
    else:
        return Response({
            'message': "You are not allowed to modify a coin"
        })


@api_view(['POST'])
def purchase_product(request):
    """
    calculates the total amount
    Checks if amount is >= product price
    check if user requires a balance
    check if balance is available
    Proceed to making a purchase
    """
    try:
        logger.info('*******-- START --*******')
        product = Product.objects.filter(id=request.data['product']).first()
        quantity = request.data['quantity']
        purchase_coins = request.data['purchase_coins']

        if not product:
            return Response({
                'message': 'Product does not exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        logger.info(f'Product available = {product.product_count}. Requested quantity = {quantity}')
        if int(product.product_count) - int(quantity) <= 0:

            return Response({
                'message': f'Product is not enough. Only {product.product_count} available.'
            }, status=status.HTTP_400_BAD_REQUEST)
        total_coins_value = get_total_purchase_coins_value(purchase_coins)
        logger.info(f'total coins value={total_coins_value}')
        total_products_value = get_products_value(product.price, quantity)
        logger.info(f'total_product_value={total_products_value}')
        if total_products_value > total_coins_value:
            return Response({
                'message': 'You do not have enough coins to purchase this product'
            }, status=status.HTTP_400_BAD_REQUEST)
        coins_balance = calculate_balance(total_coins_value, total_products_value)

        purchase_balance = get_balance(coins_balance)
        logger.info(f'purchase_balance- {purchase_balance}')

        logger.info(f'--- Make a purchase ---')
        make_purchase(product, quantity, purchase_coins)

        if purchase_balance == 0:
            return Response({
                "message": "Thank you for your purchase",
                "balance": "Your balance is 0"
            })

        logger.info('--- Update coins in the vending machine')
        for slug in list(purchase_balance):
            coins = Coins.objects.filter(coin_type__slug=slug).first()
            if coins.coin_count > 0:
                coins.coin_count -= int(purchase_balance[slug])
                coins.save()

        return Response({
            'message': "Thank you for your purchase",
            'balance': f'Your coin balance breakdown is as follows: {purchase_balance}'
        })

    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')
        return Response({
            'message': {str(e)}
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_available_coins(request):
    available_coins = get_available_coins()
    total_change_available, e = is_balance_enough(available_coins, 0)
    return Response({
        'available_coins': available_coins,
        'total_change_amount_available': total_change_available
    })
