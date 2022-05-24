from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import CreateProductSerializer, ProductSerializer, ProductTypeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Product, ProductType
from .utils import *
import logging

logger = logging.getLogger('products-logger')


class ProductTypeViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    if request.user.is_staff:

        product_serializer = CreateProductSerializer(data=request.data)
        if product_serializer.is_valid():
            _product = product_serializer.create()
            response = Response()
            _prod = Product.objects.filter(id=_product.id).first()
            response.data = {
                'user': ProductSerializer(_prod).data,
                'success': 'Product added successfully'
                }
            return response
        else:
            return Response({
                'message': product_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'You are not authorized to create a product'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_products(request):
    products = Product.objects.all()
    return Response({
        "data": ProductSerializer(products, many=True).data,
        "message": 'Products fetched successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_single_product(request, product_id):
    product = Product.objects.get(id=product_id)

    return Response({
        "data":    ProductSerializer(product).data,
        "message": 'Product fetched successfully'
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    if request.user.is_staff:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({
                'message': 'Product was not found'
            }, status=status.HTTP_404_NOT_FOUND)

        product_serializer = CreateProductSerializer(instance=product, data=request.data)
        if product_serializer.is_valid():
            _product = product_serializer.save()
            response = Response()
            response.data = {
                'user':    ProductSerializer(product).data,
                'success': 'Product added successfully'
            }
            return response
    else:
        return Response({
            'message': "You are not allowed to modify a product"
        })


