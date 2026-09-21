from django.shortcuts import render, get_object_or_404
from .models import Event, Registration, EventRequest


def event_list(request):
    events = Event.objects.all().order_by('date', 'time')
    return render(
        request,
        'events/event_list.html',
        {'events': events}
    )


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(
        request,
        'events/event_detail.html',
        {'event': event}
    )


def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    registered_count = Registration.objects.filter(
        event=event
    ).count()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not name or not email or not phone:
            return render(
                request,
                'events/register.html',
                {
                    'event': event,
                    'error': 'Please fill in all fields.'
                }
            )

        if registered_count >= event.capacity:
            return render(
                request,
                'events/register.html',
                {
                    'event': event,
                    'error': 'Sorry, this event is already full.'
                }
            )

        already_registered = Registration.objects.filter(
            event=event,
            email=email
        ).exists()

        if already_registered:
            return render(
                request,
                'events/register.html',
                {
                    'event': event,
                    'error': 'You are already registered for this event.'
                }
            )

        Registration.objects.create(
            event=event,
            name=name,
            email=email,
            phone=phone
        )

        return render(
            request,
            'events/registration_success.html',
            {'event': event}
        )

    return render(
        request,
        'events/register.html',
        {'event': event}
    )


def event_request(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        event_name = request.POST.get('event_name', '').strip()
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        location = request.POST.get('location', '').strip()
        expected_guests = request.POST.get('expected_guests')
        event_type = request.POST.get('event_type', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([
            name,
            email,
            phone,
            event_name,
            event_date,
            event_time,
            location,
            expected_guests,
            event_type,
            message
        ]):
            return render(
                request,
                'events/event_request.html',
                {'error': 'Please fill in all fields.'}
            )

        EventRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            event_name=event_name,
            event_date=event_date,
            event_time=event_time,
            location=location,
            expected_guests=expected_guests,
            event_type=event_type,
            message=message
        )

        return render(
            request,
            'events/event_request_success.html'
        )

    return render(
        request,
        'events/event_request.html'
    )
