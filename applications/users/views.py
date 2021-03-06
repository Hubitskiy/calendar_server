from django.contrib.auth.tokens import default_token_generator

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.serializers import RefreshToken

from djoser.views import UserCreateView as DjoserUserCreateView
from djoser import signals
from djoser.conf import settings
from djoser.compat import get_user_email

from .serializer import UserCreateSerializer, JWTAuthenticationSerializer, UserActivateSerializer


class JWTAuthenticationView(TokenViewBase):

    serializer_class = JWTAuthenticationSerializer
    permission_classes = [AllowAny]


class CreateUserView(DjoserUserCreateView):

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data=request.data)

        return Response(headers=headers, status=status.HTTP_204_NO_CONTENT)


class ActivateUserView(CreateModelMixin, GenericViewSet):

    serializer_class = UserActivateSerializer
    permission_classes = [AllowAny]
    token_generator = default_token_generator

    @staticmethod
    def __after_create(user_instance):
        refresh = RefreshToken.for_user(user_instance)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = self.__after_create(serializer.instance)
        headers = self.get_success_headers(data=request.data)

        return Response(headers=headers, status=status.HTTP_200_OK, data=data)
