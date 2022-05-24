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
