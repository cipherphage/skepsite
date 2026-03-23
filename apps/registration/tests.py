import json
import uuid
from datetime import date, time
from decimal import Decimal

from django.test import TestCase, Client

from apps.events.models import Event
from apps.registration.models import Registration


class RegistrationGatewayTest(TestCase):
    def test_gateway_returns_200(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_gateway_contains_role_cards(self):
        response = self.client.get('/register/')
        self.assertContains(response, 'reg-card--attendee')
        self.assertContains(response, 'reg-card--presenter')
        self.assertContains(response, 'reg-card--volunteer')

    def test_gateway_contains_decoration_image(self):
        response = self.client.get('/register/')
        self.assertContains(response, 'gateway-decoration.svg')

    def test_gateway_uses_correct_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'registration/gateway.html')


class WizardPageTest(TestCase):
    def test_attendee_wizard_returns_200(self):
        response = self.client.get('/register/attendee/')
        self.assertEqual(response.status_code, 200)

    def test_presenter_wizard_returns_200(self):
        response = self.client.get('/register/presenter/')
        self.assertEqual(response.status_code, 200)

    def test_volunteer_wizard_returns_200(self):
        response = self.client.get('/register/volunteer/')
        self.assertEqual(response.status_code, 200)


class RegistrationSubmitBaseTest(TestCase):
    """Base class with common helpers for registration submit tests."""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def _submit(self, reg_type, data):
        return self.client.post(
            f'/register/submit/{reg_type}/',
            data=json.dumps(data),
            content_type='application/json',
        )

    def _valid_attendee_data(self, **overrides):
        data = {
            'first_name': 'Ada',
            'last_name': 'Lovelace',
            'email': 'ada@example.com',
            'gdpr_consent': True,
            'code_of_conduct_accepted': True,
            'attendance_format': 'in_person',
        }
        data.update(overrides)
        return data

    def _valid_presenter_data(self, **overrides):
        data = self._valid_attendee_data(
            email='presenter@example.com',
            talk_title='The Analytical Engine',
            talk_duration='30',
            talk_description='A talk about early computing.',
            audience_level='general',
        )
        data.update(overrides)
        return data

    def _valid_volunteer_data(self, **overrides):
        data = self._valid_attendee_data(
            email='volunteer@example.com',
            volunteer_roles=['registration', 'setup'],
            volunteer_availability='full_day',
        )
        data.update(overrides)
        return data


class AttendeeSubmitTest(RegistrationSubmitBaseTest):
    def test_valid_attendee_submission_succeeds(self):
        response = self._submit('attendee', self._valid_attendee_data())
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['success'])
        self.assertIn('confirmation_url', body)
        self.assertEqual(body['status'], 'confirmed')

    def test_attendee_creates_registration_record(self):
        self._submit('attendee', self._valid_attendee_data())
        self.assertEqual(Registration.objects.count(), 1)
        reg = Registration.objects.first()
        self.assertEqual(reg.first_name, 'Ada')
        self.assertEqual(reg.registration_type, 'attendee')


class PresenterSubmitTest(RegistrationSubmitBaseTest):
    def test_valid_presenter_submission_succeeds(self):
        response = self._submit('presenter', self._valid_presenter_data())
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['success'])

    def test_presenter_saves_talk_fields(self):
        self._submit('presenter', self._valid_presenter_data())
        reg = Registration.objects.first()
        self.assertEqual(reg.talk_title, 'The Analytical Engine')
        self.assertEqual(reg.talk_duration, '30')


class VolunteerSubmitTest(RegistrationSubmitBaseTest):
    def test_valid_volunteer_submission_succeeds(self):
        response = self._submit('volunteer', self._valid_volunteer_data())
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['success'])

    def test_volunteer_saves_roles(self):
        self._submit('volunteer', self._valid_volunteer_data())
        reg = Registration.objects.first()
        self.assertIn('registration', reg.volunteer_roles)
        self.assertIn('setup', reg.volunteer_roles)


class RegistrationValidationTest(RegistrationSubmitBaseTest):
    def test_missing_first_name_fails(self):
        data = self._valid_attendee_data(first_name='')
        response = self._submit('attendee', data)
        self.assertEqual(response.status_code, 422)
        body = response.json()
        self.assertIn('first_name', body['errors'])

    def test_missing_last_name_fails(self):
        data = self._valid_attendee_data(last_name='')
        response = self._submit('attendee', data)
        self.assertEqual(response.status_code, 422)

    def test_missing_email_fails(self):
        data = self._valid_attendee_data(email='')
        response = self._submit('attendee', data)
        self.assertEqual(response.status_code, 422)

    def test_invalid_email_fails(self):
        data = self._valid_attendee_data(email='not-an-email')
        response = self._submit('attendee', data)
        self.assertEqual(response.status_code, 422)
        body = response.json()
        self.assertIn('email', body['errors'])

    def test_duplicate_email_fails(self):
        self._submit('attendee', self._valid_attendee_data())
        response = self._submit('attendee', self._valid_attendee_data())
        self.assertEqual(response.status_code, 422)
        body = response.json()
        self.assertIn('email', body['errors'])

    def test_without_gdpr_consent_fails(self):
        data = self._valid_attendee_data(gdpr_consent=False)
        response = self._submit('attendee', data)
        self.assertEqual(response.status_code, 422)
        body = response.json()
        self.assertIn('gdpr_consent', body['errors'])

    def test_without_code_of_conduct_fails(self):
        data = self._valid_attendee_data(code_of_conduct_accepted=False)
        response = self._submit('attendee', data)
        self.assertEqual(response.status_code, 422)
        body = response.json()
        self.assertIn('code_of_conduct_accepted', body['errors'])

    def test_invalid_registration_type_fails(self):
        response = self._submit('invalid', self._valid_attendee_data())
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_body_fails(self):
        response = self.client.post(
            '/register/submit/attendee/',
            data='not json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


class ConfirmationPageTest(TestCase):
    def setUp(self):
        self.registration = Registration.objects.create(
            registration_type='attendee',
            first_name='Ada',
            last_name='Lovelace',
            email='ada@example.com',
            gdpr_consent=True,
            code_of_conduct_accepted=True,
        )

    def test_confirmation_returns_200_for_valid_token(self):
        url = f'/register/confirmation/{self.registration.confirmation_token}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_confirmation_returns_404_for_invalid_token(self):
        fake_token = uuid.uuid4()
        url = f'/register/confirmation/{fake_token}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CalendarICSTest(TestCase):
    def setUp(self):
        # Deactivate any seeded events from migrations
        Event.objects.update(is_active=False)
        self.event = Event.objects.create(
            name='Skepticamp NYC 2025',
            date=date(2025, 12, 6),
            start_time=time(9, 30),
            end_time=time(18, 0),
            venue_name='Test Venue',
            venue_address='123 Test St',
            venue_city='New York, NY',
            is_active=True,
        )
        self.registration = Registration.objects.create(
            registration_type='attendee',
            first_name='Ada',
            last_name='Lovelace',
            email='ada@example.com',
            gdpr_consent=True,
            code_of_conduct_accepted=True,
        )

    def test_calendar_ics_returns_200(self):
        url = f'/register/confirmation/{self.registration.confirmation_token}/calendar.ics'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/calendar; charset=utf-8')

    def test_calendar_ics_contains_vevent(self):
        url = f'/register/confirmation/{self.registration.confirmation_token}/calendar.ics'
        response = self.client.get(url)
        content = response.content.decode()
        self.assertIn('BEGIN:VEVENT', content)
        self.assertIn('Skepticamp NYC 2025', content)

    def test_calendar_ics_404_without_event(self):
        self.event.is_active = False
        self.event.save()
        url = f'/register/confirmation/{self.registration.confirmation_token}/calendar.ics'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_calendar_ics_404_for_invalid_token(self):
        fake_token = uuid.uuid4()
        url = f'/register/confirmation/{fake_token}/calendar.ics'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CapacityWaitlistTest(RegistrationSubmitBaseTest):
    def setUp(self):
        super().setUp()
        # Deactivate any seeded events from migrations
        Event.objects.update(is_active=False)
        self.event = Event.objects.create(
            name='Skepticamp NYC 2025',
            date=date(2025, 12, 6),
            start_time=time(9, 30),
            end_time=time(18, 0),
            venue_name='Test Venue',
            venue_address='123 Test St',
            venue_city='New York, NY',
            is_active=True,
            max_capacity=1,
        )

    def test_first_registration_is_confirmed(self):
        response = self._submit('attendee', self._valid_attendee_data())
        body = response.json()
        self.assertEqual(body['status'], 'confirmed')

    def test_over_capacity_registration_is_waitlisted(self):
        # Fill to capacity
        self._submit('attendee', self._valid_attendee_data())
        # Next in-person registration should be waitlisted
        data = self._valid_attendee_data(email='second@example.com')
        response = self._submit('attendee', data)
        body = response.json()
        self.assertEqual(body['status'], 'waitlisted')


class DonationFieldTest(RegistrationSubmitBaseTest):
    def test_donation_amount_saved_correctly(self):
        data = self._valid_attendee_data(donation_amount='25')
        self._submit('attendee', data)
        reg = Registration.objects.first()
        self.assertEqual(reg.donation_amount, Decimal('25'))

    def test_donation_amount_can_be_null(self):
        data = self._valid_attendee_data()
        self._submit('attendee', data)
        reg = Registration.objects.first()
        self.assertIsNone(reg.donation_amount)

    def test_donation_amount_can_be_empty_string(self):
        data = self._valid_attendee_data(donation_amount='')
        self._submit('attendee', data)
        reg = Registration.objects.first()
        self.assertIsNone(reg.donation_amount)
