from datetime import timedelta


class DateSendInvitation:

    def __init__(self, data):
        self.validated_data = data

    @classmethod
    def prepare_for_recount(cls, validated_data, instance):
        validated_data.setdefault("time_period", instance.time_period)
        validated_data.setdefault("event_date", instance.event_date)

        return cls(validated_data)

    def __call__(self, *args, **kwargs):
        time_period = self.validated_data["time_period"]
        event_date = self.validated_data["event_date"]
        time_period = {
                'HOUR': event_date - timedelta(hours=1),
                'DAY':  event_date - timedelta(days=1),
                'WEEK': event_date - timedelta(weeks=1),
            }.get(time_period, event_date)

        return time_period
