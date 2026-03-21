import json
import re
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from apps.events.models import Event
from .models import Registration
from apps.communications.email_utils import send_registration_confirmation


def _get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


class RegistrationGatewayView(TemplateView):
    template_name = 'registration/gateway.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = Event.objects.filter(is_active=True).first()
        return ctx


class AttendeeWizardView(TemplateView):
    template_name = 'registration/attendee_wizard.html'


class PresenterWizardView(TemplateView):
    template_name = 'registration/presenter_wizard.html'


class VolunteerWizardView(TemplateView):
    template_name = 'registration/volunteer_wizard.html'


@method_decorator(csrf_protect, name='dispatch')
class RegistrationSubmitView(View):
    """JSON endpoint — Vue wizard POSTs here."""

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def post(self, request, registration_type):
        if registration_type not in ('attendee', 'presenter', 'volunteer'):
            return JsonResponse({'success': False, 'error': 'Invalid registration type.'}, status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid request data.'}, status=400)

        # Server-side email validation
        email = data.get('email', '').strip().lower()
        if not self._is_valid_email(email):
            return JsonResponse({'success': False, 'errors': {'email': 'Please enter a valid email address.'}}, status=422)

        # Required fields check
        errors = {}
        for field in self.REQUIRED_FIELDS:
            if not data.get(field, '').strip():
                errors[field] = 'This field is required.'
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=422)

        # GDPR consent required
        if not data.get('gdpr_consent'):
            return JsonResponse(
                {'success': False, 'errors': {'gdpr_consent': 'You must accept the privacy policy to register.'}},
                status=422,
            )

        # Code of conduct required
        if not data.get('code_of_conduct_accepted'):
            return JsonResponse(
                {'success': False, 'errors': {'code_of_conduct_accepted': 'You must accept the code of conduct to register.'}},
                status=422,
            )

        # Duplicate check
        if Registration.objects.filter(email=email, registration_type=registration_type).exists():
            return JsonResponse({
                'success': False,
                'errors': {
                    'email': (
                        f'This email is already registered as an {registration_type}. '
                        'If you need to make changes, please contact us at admin@skepticampnyc.org.'
                    )
                }
            }, status=422)

        # Capacity check for in-person attendees
        event = Event.objects.filter(is_active=True).first()
        status = Registration.STATUS_CONFIRMED
        if event and event.is_at_capacity and data.get('attendance_format') == 'in_person':
            status = Registration.STATUS_WAITLISTED

        # Build registration kwargs
        reg_kwargs = {
            'registration_type': registration_type,
            'status': status,
            'first_name': data.get('first_name', '').strip(),
            'last_name': data.get('last_name', '').strip(),
            'email': email,
            'phone': data.get('phone', '').strip(),
            'how_heard': data.get('how_heard', '').strip(),
            'attendance_format': data.get('attendance_format', '').strip(),
            'dietary_needs': data.get('dietary_needs', []),
            'accessibility_needs': data.get('accessibility_needs', '').strip(),
            'gdpr_consent': bool(data.get('gdpr_consent')),
            'code_of_conduct_accepted': bool(data.get('code_of_conduct_accepted')),
            'ip_address': _get_client_ip(request) or None,
        }

        if data.get('donation_amount'):
            try:
                reg_kwargs['donation_amount'] = float(data['donation_amount'])
            except (ValueError, TypeError):
                pass

        if registration_type == Registration.PRESENTER:
            reg_kwargs.update({
                'talk_title': data.get('talk_title', '').strip(),
                'talk_duration': data.get('talk_duration', '').strip(),
                'talk_description': data.get('talk_description', '').strip(),
                'audience_level': data.get('audience_level', '').strip(),
                'bio': data.get('bio', '').strip(),
                'affiliation': data.get('affiliation', '').strip(),
                'presented_before': data.get('presented_before'),
                'av_needs': data.get('av_needs', []),
                'remote_presenting': data.get('remote_presenting'),
                'preferred_session_time': data.get('preferred_session_time', '').strip(),
            })
        elif registration_type == Registration.VOLUNTEER:
            reg_kwargs.update({
                'volunteer_roles': data.get('volunteer_roles', []),
                'volunteer_notes': data.get('volunteer_notes', '').strip(),
                'volunteer_availability': data.get('volunteer_availability', '').strip(),
                'volunteer_shift_details': data.get('volunteer_shift_details', '').strip(),
            })

        registration = Registration.objects.create(**reg_kwargs)
        send_registration_confirmation(registration)

        return JsonResponse({
            'success': True,
            'confirmation_url': registration.get_absolute_url(),
            'status': registration.status,
            'confirmation_number': registration.confirmation_number,
        })

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class ConfirmationView(View):
    template_name = 'registration/confirmation.html'

    def get(self, request, token):
        registration = get_object_or_404(Registration, confirmation_token=token)
        event = Event.objects.filter(is_active=True).first()
        return render(request, self.template_name, {
            'registration': registration,
            'event': event,
        })


class CalendarICSView(View):
    """Returns an ICS calendar file for the event."""

    def get(self, request, token):
        registration = get_object_or_404(Registration, confirmation_token=token)
        event = Event.objects.filter(is_active=True).first()
        if not event:
            from django.http import Http404
            raise Http404

        ics_content = self._build_ics(event, registration)
        response = HttpResponse(ics_content, content_type='text/calendar; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="skepticamp-nyc-2025.ics"'
        return response

    @staticmethod
    def _build_ics(event, registration) -> str:
        from datetime import datetime
        try:
            from zoneinfo import ZoneInfo
            tz = ZoneInfo('America/New_York')
            start = datetime.combine(event.date, event.start_time, tzinfo=tz)
            end = datetime.combine(event.date, event.end_time, tzinfo=tz)
        except ImportError:
            # Fallback: use naive datetimes (Python < 3.9)
            start = datetime.combine(event.date, event.start_time)
            end = datetime.combine(event.date, event.end_time)

        fmt = '%Y%m%dT%H%M%S'

        return (
            'BEGIN:VCALENDAR\r\n'
            'VERSION:2.0\r\n'
            'PRODID:-//Skepticamp NYC//EN\r\n'
            'CALSCALE:GREGORIAN\r\n'
            'METHOD:PUBLISH\r\n'
            'BEGIN:VEVENT\r\n'
            f'DTSTART;TZID=America/New_York:{start.strftime(fmt)}\r\n'
            f'DTEND;TZID=America/New_York:{end.strftime(fmt)}\r\n'
            f'SUMMARY:{event.name}\r\n'
            f'LOCATION:{event.full_venue_address}\r\n'
            f'DESCRIPTION:Skepticamp NYC — Share the Apple of Knowledge.\\nConfirmation: {registration.confirmation_number}\r\n'
            f'UID:{registration.confirmation_token}@skepticampnyc.org\r\n'
            'END:VEVENT\r\n'
            'END:VCALENDAR\r\n'
        )
