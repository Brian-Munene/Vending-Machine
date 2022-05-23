import datetime
import jwt
import environ

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
