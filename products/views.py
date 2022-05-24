from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, exceptions, viewsets
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


class CreateProduct(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        return Response({
            'Message': 'Register a new user'
        })

    def post(self, request):
        user_serializer = CreateProductSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.create()
            response = Response()
            # response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            # _user = CustomUser.objects.filter(email=user_serializer.data['email']).first()
            # response.data = {
            #     'user': CustomUserSerializer(_user).data,
            #     'access_token': access_token,
            #     'success': 'Registration successful'
            #     }
            return response
        else:
            return Response({
                'message': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
