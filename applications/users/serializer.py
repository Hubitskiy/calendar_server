from django.contrib.auth import authenticate
from django.core import exceptions as django_exceptions
from django.db import transaction, IntegrityError
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.conf import settings as djoser_settings

from .models import User


class JWTAuthenticationSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        authenticate_credentials = {}
        authenticate_credentials.update({"email": attrs["email"], "password": attrs["password"]})

        authenticate_credentials["request"] = self.context["request"]
        user = authenticate(**authenticate_credentials)

        if user is None:
            raise exceptions.AuthenticationFailed("No active account with given credentials")

        if not user.is_active:
            raise serializers.ValidationError("You should complete registration")

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


class UserCreateSerializer(DjoserUserCreateSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, required=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user.exists():
            raise serializers.ValidationError("User with given credentials already exist")
        return value

    def validate_password(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({
                'password': serializer_error['non_field_errors']
            })

        return attrs

    def create(self, validated_data):
        try:
            user = self._perform_create(validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')

        return user

    def _perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if djoser_settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user

    def update(self, instance, validated_data):
        pass
