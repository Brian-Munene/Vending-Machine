from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import CoinTypeSerializer, CoinSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging

from .models import CoinType, Coins

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
        coin = Coins.objects.filter(id=coin_id).first()
        print(coin)
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
