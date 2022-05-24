import datetime
import jwt
import environ
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from .models import CustomUser

env = environ.Env()
environ.Env.read_env()


def generate_access_token(user):

    access_token_payload = {
        'user_id': str(user.public_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              env('SECRET_KEY'), algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': str(user.public_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, env('SECRET_KEY'), algorithm='HS256')

    return refresh_token


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        authorization_heaader = request.headers.get('Authorization')

        if not authorization_heaader:
            return None
        try:
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, env('SECRET_KEY'), algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = CustomUser.objects.filter(public_id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        # self.enforce_csrf(request)
        return (user, None)

    def enforce_csrf(self, request):
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
