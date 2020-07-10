from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from djoser.views import UserCreateView as DjoserUserCreateView
from djoser import signals
from djoser.conf import settings

from .serializer import UserCreateSerializer, JWTAuthenticationSerializer


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
        if settings.SEND_ACTIVATION_EMAIL:
            from logging import warning
            warning(f"SEND EMAIL {user.email}")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data=request.data)
        return Response(headers=headers, status=status.HTTP_204_NO_CONTENT)

