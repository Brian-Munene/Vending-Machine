from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, exceptions
from .serializers import RegisterCustomUserSerializer, CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import CustomUser
from .utils import *
import logging

logger = logging.getLogger('accounts-logger')


class RegisterUsers(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        return Response({
            'Message': 'Register a new user'
        })

    def post(self, request):
        user_serializer = RegisterCustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.create()
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            response = Response()
            response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            _user = CustomUser.objects.filter(email=user_serializer.data['email']).first()
            response.data = {
                'user': CustomUserSerializer(_user).data,
                'access_token': access_token,
                'success': 'Registration successful'
                }
            return response
        else:
            return Response({
                'message': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = CustomUser.objects.filter(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = CustomUserSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }

    return response
