"""
Tests for the registrant sign-in flow: login, dashboard, presentation edit, logout.
"""
from datetime import date, time
from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta

from apps.events.models import Event
from apps.registration.models import Registration


def _create_event(**overrides):
    defaults = dict(
        name='Skepticamp NYC 2025',
        date=date(2025, 12, 6),
        start_time=time(9, 30),
        end_time=time(18, 0),
        venue_name='Test Venue',
        venue_address='123 Test St',
        venue_city='New York, NY',
        is_active=True,
    )
    defaults.update(overrides)
    return Event.objects.create(**defaults)


def _create_registration(reg_type='attendee', **overrides):
    defaults = dict(
        registration_type=reg_type,
        first_name='Jane',
        last_name='Doe',
        email='jane@example.com',
        gdpr_consent=True,
        code_of_conduct_accepted=True,
    )
    defaults.update(overrides)
    return Registration.objects.create(**defaults)


class RegistrantLoginViewTest(TestCase):
    def setUp(self):
        self.reg = _create_registration()

    def test_login_page_returns_200(self):
        response = self.client.get('/my-registration/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_contains_form(self):
        response = self.client.get('/my-registration/')
        self.assertContains(response, '<form')
        self.assertContains(response, 'email')
        self.assertContains(response, 'confirmation_number')

    def test_login_with_valid_credentials_redirects_to_dashboard(self):
        response = self.client.post('/my-registration/', {
            'email': self.reg.email,
            'confirmation_number': self.reg.confirmation_number,
        })
        self.assertRedirects(response, '/my-registration/dashboard/')

    def test_login_sets_session(self):
        self.client.post('/my-registration/', {
            'email': self.reg.email,
            'confirmation_number': self.reg.confirmation_number,
        })
        self.assertEqual(self.client.session['registration_id'], self.reg.pk)

    def test_login_with_wrong_confirmation_number_shows_error(self):
        response = self.client.post('/my-registration/', {
            'email': self.reg.email,
            'confirmation_number': 'WRONG-NUMBER',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No registration found')

    def test_login_with_wrong_email_shows_error(self):
        response = self.client.post('/my-registration/', {
            'email': 'wrong@example.com',
            'confirmation_number': self.reg.confirmation_number,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No registration found')

    def test_login_with_empty_fields_shows_errors(self):
        response = self.client.post('/my-registration/', {
            'email': '',
            'confirmation_number': '',
        })
        self.assertEqual(response.status_code, 200)

    def test_already_signed_in_redirects_to_dashboard(self):
        session = self.client.session
        session['registration_id'] = self.reg.pk
        session.save()
        response = self.client.get('/my-registration/')
        self.assertRedirects(response, '/my-registration/dashboard/')

    def test_login_is_case_insensitive_for_email(self):
        response = self.client.post('/my-registration/', {
            'email': 'JANE@EXAMPLE.COM',
            'confirmation_number': self.reg.confirmation_number,
        })
        self.assertRedirects(response, '/my-registration/dashboard/')

    def test_login_is_case_insensitive_for_confirmation_number(self):
        """Confirmation numbers are uppercased before lookup."""
        response = self.client.post('/my-registration/', {
            'email': self.reg.email,
            'confirmation_number': self.reg.confirmation_number.lower(),
        })
        self.assertRedirects(response, '/my-registration/dashboard/')


class RegistrantDashboardViewTest(TestCase):
    def setUp(self):
        self.event = _create_event()
        self.reg = _create_registration()
        # Sign in
        session = self.client.session
        session['registration_id'] = self.reg.pk
        session.save()

    def test_dashboard_returns_200_when_signed_in(self):
        response = self.client.get('/my-registration/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_redirects_when_not_signed_in(self):
        # Fresh client, no session
        client = Client()
        response = client.get('/my-registration/dashboard/')
        self.assertRedirects(response, '/my-registration/')

    def test_dashboard_shows_registration_details(self):
        response = self.client.get('/my-registration/dashboard/')
        self.assertContains(response, self.reg.first_name)
        self.assertContains(response, self.reg.confirmation_number)

    def test_dashboard_shows_event_info(self):
        response = self.client.get('/my-registration/dashboard/')
        self.assertContains(response, self.event.name)

    def test_dashboard_shows_presenter_edit_link_for_presenter(self):
        presenter = _create_registration(
            reg_type='presenter',
            email='presenter@example.com',
            talk_title='My Talk',
        )
        session = self.client.session
        session['registration_id'] = presenter.pk
        session.save()
        response = self.client.get('/my-registration/dashboard/')
        self.assertContains(response, 'presentation/edit')

    def test_dashboard_stale_session_redirects_to_login(self):
        """If the registration was deleted, the session is cleaned up."""
        self.reg.delete()
        response = self.client.get('/my-registration/dashboard/')
        self.assertRedirects(response, '/my-registration/')


class RegistrantLogoutViewTest(TestCase):
    def setUp(self):
        self.reg = _create_registration()
        session = self.client.session
        session['registration_id'] = self.reg.pk
        session.save()

    def test_logout_clears_session(self):
        self.client.get('/my-registration/logout/')
        self.assertNotIn('registration_id', self.client.session)

    def test_logout_redirects_to_login(self):
        response = self.client.get('/my-registration/logout/')
        self.assertRedirects(response, '/my-registration/')

    def test_logout_via_post(self):
        response = self.client.post('/my-registration/logout/')
        self.assertRedirects(response, '/my-registration/')
        self.assertNotIn('registration_id', self.client.session)


class PresentationEditViewTest(TestCase):
    def setUp(self):
        # Deactivate any seeded events from migrations
        Event.objects.update(is_active=False)
        self.event = _create_event(
            editing_deadline=timezone.now() + timedelta(days=7),
        )
        self.presenter = _create_registration(
            reg_type='presenter',
            email='presenter@example.com',
            talk_title='Original Title',
            talk_description='Original description',
        )
        session = self.client.session
        session['registration_id'] = self.presenter.pk
        session.save()

    def test_edit_page_returns_200_for_presenter(self):
        response = self.client.get('/my-registration/presentation/edit/')
        self.assertEqual(response.status_code, 200)

    def test_edit_page_redirects_non_presenter_to_dashboard(self):
        attendee = _create_registration(
            reg_type='attendee',
            email='attendee@example.com',
        )
        session = self.client.session
        session['registration_id'] = attendee.pk
        session.save()
        response = self.client.get('/my-registration/presentation/edit/')
        self.assertRedirects(response, '/my-registration/dashboard/')

    def test_edit_page_redirects_unauthenticated_to_login(self):
        client = Client()
        response = client.get('/my-registration/presentation/edit/')
        self.assertRedirects(response, '/my-registration/')

    def test_edit_page_contains_form_with_current_data(self):
        response = self.client.get('/my-registration/presentation/edit/')
        self.assertContains(response, 'Original Title')

    def test_edit_post_saves_changes(self):
        self.client.post('/my-registration/presentation/edit/', {
            'talk_title': 'Updated Title',
            'talk_description': 'Updated description',
            'talk_duration': '30',
            'audience_level': 'intermediate',
            'av_needs': [],
            'bio': 'A bio',
            'affiliation': 'Test Org',
        })
        self.presenter.refresh_from_db()
        self.assertEqual(self.presenter.talk_title, 'Updated Title')

    def test_edit_post_redirects_to_dashboard_on_success(self):
        response = self.client.post('/my-registration/presentation/edit/', {
            'talk_title': 'Updated Title',
            'talk_description': 'Updated description',
            'talk_duration': '30',
            'audience_level': 'intermediate',
            'av_needs': [],
            'bio': '',
            'affiliation': '',
        })
        self.assertRedirects(response, '/my-registration/dashboard/')

    def test_edit_blocked_after_deadline(self):
        """Server-side deadline enforcement: editing should be refused after deadline passes."""
        self.event.editing_deadline = timezone.now() - timedelta(hours=1)
        self.event.save()
        response = self.client.get('/my-registration/presentation/edit/')
        self.assertRedirects(response, '/my-registration/dashboard/')

    def test_edit_post_blocked_after_deadline(self):
        """POST should also be refused after deadline."""
        self.event.editing_deadline = timezone.now() - timedelta(hours=1)
        self.event.save()
        response = self.client.post('/my-registration/presentation/edit/', {
            'talk_title': 'Sneaky Late Edit',
            'talk_description': 'Trying to edit after deadline',
            'talk_duration': '15',
            'audience_level': 'beginner',
            'av_needs': [],
            'bio': '',
            'affiliation': '',
        })
        self.assertRedirects(response, '/my-registration/dashboard/')
        self.presenter.refresh_from_db()
        self.assertEqual(self.presenter.talk_title, 'Original Title')

    def test_edit_allowed_when_no_deadline_set(self):
        """If no editing_deadline is set on the event, editing should be open."""
        self.event.editing_deadline = None
        self.event.save()
        response = self.client.get('/my-registration/presentation/edit/')
        self.assertEqual(response.status_code, 200)

    def test_edit_post_with_empty_title_shows_error(self):
        response = self.client.post('/my-registration/presentation/edit/', {
            'talk_title': '',
            'talk_description': 'Description',
            'talk_duration': '15',
            'audience_level': 'beginner',
            'av_needs': [],
            'bio': '',
            'affiliation': '',
        })
        self.assertEqual(response.status_code, 200)  # Re-renders form with errors
        self.presenter.refresh_from_db()
        self.assertEqual(self.presenter.talk_title, 'Original Title')
