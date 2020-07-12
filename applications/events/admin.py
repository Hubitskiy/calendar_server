from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):

    list_display = [
        'events_title',
        'description',
        'date_to_send_invitations',
        'user',
    ]

    filter_horizontal = ()


admin.site.register(Event, EventAdmin)
# Register your models here.
