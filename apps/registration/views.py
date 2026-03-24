import json
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from apps.events.models import Event
from .models import Registration
from .forms import RegistrantLoginForm, PresentationEditForm
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


# ---------------------------------------------------------------------------
# Registrant sign-in flow
# ---------------------------------------------------------------------------

def _get_registrant(request):
    """Retrieve the logged-in registrant from session, or None."""
    registration_id = request.session.get('registration_id')
    if registration_id is None:
        return None
    try:
        return Registration.objects.get(pk=registration_id)
    except Registration.DoesNotExist:
        # Stale session — clean up
        request.session.pop('registration_id', None)
        return None


@method_decorator(csrf_protect, name='dispatch')
class RegistrantLoginView(View):
    """Sign in with email + confirmation number."""
    template_name = 'registration/registrant_login.html'

    def get(self, request):
        # If already signed in, redirect straight to dashboard
        if _get_registrant(request) is not None:
            return redirect('registrant:dashboard')
        form = RegistrantLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrantLoginForm(request.POST)
        if form.is_valid():
            registration = form.cleaned_data['registration']
            request.session['registration_id'] = registration.pk
            return redirect('registrant:dashboard')
        return render(request, self.template_name, {'form': form})


class RegistrantDashboardView(View):
    """Dashboard showing registration details for signed-in registrant."""
    template_name = 'registration/registrant_dashboard.html'

    def get(self, request):
        registration = _get_registrant(request)
        if registration is None:
            return redirect('registrant:login')

        event = Event.objects.filter(is_active=True).first()

        # Build deadline ISO string for the countdown component
        editing_deadline_iso = None
        editing_open = True
        if event and event.editing_deadline:
            editing_deadline_iso = event.editing_deadline.isoformat()
            editing_open = event.is_editing_open

        return render(request, self.template_name, {
            'registration': registration,
            'event': event,
            'editing_deadline_iso': editing_deadline_iso,
            'editing_open': editing_open,
        })


class RegistrantLogoutView(View):
    """Sign out the registrant."""
    def post(self, request):
        request.session.pop('registration_id', None)
        return redirect('registrant:login')

    def get(self, request):
        request.session.pop('registration_id', None)
        return redirect('registrant:login')


@method_decorator(csrf_protect, name='dispatch')
class PresentationEditView(View):
    """Edit presentation details — only for presenters, before deadline."""
    template_name = 'registration/presentation_edit.html'

    def get(self, request):
        registration = _get_registrant(request)
        if registration is None:
            return redirect('registrant:login')
        if registration.registration_type != Registration.PRESENTER:
            messages.error(request, 'Only presenters can edit presentation details.')
            return redirect('registrant:dashboard')

        event = Event.objects.filter(is_active=True).first()
        if event and not event.is_editing_open:
            messages.error(request, 'The editing deadline has passed. You can no longer edit your presentation.')
            return redirect('registrant:dashboard')

        form = PresentationEditForm(instance=registration)
        editing_deadline_iso = event.editing_deadline.isoformat() if event and event.editing_deadline else None
        return render(request, self.template_name, {
            'form': form,
            'registration': registration,
            'event': event,
            'editing_deadline_iso': editing_deadline_iso,
        })

    def post(self, request):
        registration = _get_registrant(request)
        if registration is None:
            return redirect('registrant:login')
        if registration.registration_type != Registration.PRESENTER:
            messages.error(request, 'Only presenters can edit presentation details.')
            return redirect('registrant:dashboard')

        event = Event.objects.filter(is_active=True).first()
        if event and not event.is_editing_open:
            messages.error(request, 'The editing deadline has passed. You can no longer edit your presentation.')
            return redirect('registrant:dashboard')

        form = PresentationEditForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your presentation details have been updated.')
            return redirect('registrant:dashboard')

        editing_deadline_iso = event.editing_deadline.isoformat() if event and event.editing_deadline else None
        return render(request, self.template_name, {
            'form': form,
            'registration': registration,
            'event': event,
            'editing_deadline_iso': editing_deadline_iso,
        })
