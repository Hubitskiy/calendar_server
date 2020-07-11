from django_filters import rest_framework as filter

from events.models import Event


class EventFilter(filter.FilterSet):
    is_ended = filter.BooleanFilter(field_name="is_ended")

    max_date_invitation = filter.DateTimeFilter(field_name="date_to_send_invitations", lookup_expr="gte")
    min_date_invitation = filter.DateTimeFilter(field_name="date_to_send_invitations", lookup_expr="lte")

    max_event_date = filter.DateTimeFilter(field_name="event_date", lookup_expr="gte")
    min_event_date = filter.DateTimeFilter(field_name="event_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = [
            "max_event_date",
            "min_event_date",
            "max_date_invitation",
            "min_date_invitation",
            "is_ended"
        ]