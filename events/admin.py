from django import forms
from django.contrib import admin
from cloudinary.forms import CloudinaryFileField

from .models import Event, Registration, EventRequest


class EventAdminForm(forms.ModelForm):
    image = CloudinaryFileField(required=False)

    class Meta:
        model = Event
        fields = '__all__'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm


admin.site.register(Registration)


@admin.action(description='Create Event from approved request')
def create_event_from_request(modeladmin, request, queryset):
    approved_requests = queryset.filter(status='Approved')
    created_count = 0

    for event_request in approved_requests:
        Event.objects.create(
            title=event_request.event_name,
            description=event_request.message,
            date=event_request.event_date,
            time=event_request.event_time,
            location=event_request.location,
            capacity=event_request.expected_guests,
        )
        created_count += 1

    modeladmin.message_user(
        request,
        f'{created_count} event(s) created successfully.'
    )


@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = (
        'event_name',
        'name',
        'event_date',
        'event_time',
        'location',
        'expected_guests',
        'event_type',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'event_type',
        'event_date',
    )

    search_fields = (
        'event_name',
        'name',
        'email',
        'phone',
    )

    ordering = (
        'status',
        'event_date',
    )

    actions = [
        create_event_from_request,
    ]
