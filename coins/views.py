from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import CoinTypeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging

from .models import CoinType

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
