from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
import logging

logger = logging.getLogger('accounts-logger')


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            "email": {"required": True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields did not match."})
        return attrs

    def create(self):
        user = CustomUser.objects.create(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        user.set_password(self.validated_data['password'])
        user.save()

        logger.info(f'User {user.public_id} has been saved to the database')
        user.refresh_from_db()

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']