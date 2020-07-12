from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .custom_filters.custom_filters import EventFilter
from rest_framework import status
from .utils import DateSendInvitation
from .custom_permission import IsSelfUser
from .models import Event
from .serializer import CreateEventSerializer, RetrieveEventSerializer


class EventCreateView(CreateAPIView):

    serializer_class = CreateEventSerializer
    permission_classes = [IsAuthenticated]

    def _perform_create(self, serializer):
        validated_data = serializer.validated_data
        get_date_to_send_invitation = DateSendInvitation(validated_data)
        validated_data.setdefault("user", self.request.user)
        validated_data.setdefault("date_to_send_invitations", get_date_to_send_invitation())
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_event = self._perform_create(serializer)
        serializer = RetrieveEventSerializer(created_event)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventRetrieveDestroyUpdateView(RetrieveUpdateDestroyAPIView):

    serializer_class = RetrieveEventSerializer
    permission_classes = [IsAuthenticated, IsSelfUser]
    queryset = Event.objects


class EventListView(ListModelMixin, GenericViewSet):

    serializer_class = RetrieveEventSerializer
    permission_classes = [IsAuthenticated]
    queryset = Event.objects
    filter_class = EventFilter

    def get_queryset(self):
        assert self.queryset is not None

        queryset = self.queryset.filter(user_id=self.request.user.id)
        return queryset

