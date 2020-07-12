from django.db import models
from django.conf import settings


class Event(models.Model):

    TIME_PERIOD = [
        ('JUST_NOW', 'JUST_NOW'),
        ('HOUR', 'HOUR'),
        ('DAY', 'DAY'),
        ('WEEK', 'MONTH'),
    ]

    events_title = models.CharField(
        verbose_name='Events name',
        max_length=30
    )
    description = models.TextField(
        verbose_name='Events description',
        max_length=150
    )
    time_period = models.CharField(
        verbose_name='Time period for sending a notification',
        choices=TIME_PERIOD, default='JUST_NOW',
        max_length=15
    )
    event_date = models.DateTimeField(
        verbose_name='Event Date',
        blank=False,
        default=None
    )
    date_to_send_invitations = models.DateTimeField(
        verbose_name='date and time to send invitation',
        blank=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    is_sent = models.BooleanField(
        default=False
    )
    is_ended = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.events_title
