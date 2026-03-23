from datetime import date, time
from django.test import TestCase

from apps.events.models import Event
from apps.registration.models import Registration


class EventCreationTest(TestCase):
    def test_create_event_with_required_fields(self):
        event = Event.objects.create(
            name='Skepticamp NYC 2025',
            date=date(2025, 12, 6),
            start_time=time(9, 30),
            end_time=time(18, 0),
            venue_name='Test Venue',
            venue_address='151 W. 30th St, 3rd Floor',
            venue_city='New York, NY 10001',
        )
        self.assertEqual(event.name, 'Skepticamp NYC 2025')
        self.assertTrue(event.is_active)

    def test_event_str_representation(self):
        event = Event.objects.create(
            name='Skepticamp NYC 2025',
            date=date(2025, 12, 6),
            start_time=time(9, 30),
            end_time=time(18, 0),
            venue_name='Test Venue',
            venue_address='123 Test St',
            venue_city='New York, NY',
        )
        self.assertIn('Skepticamp NYC 2025', str(event))


class EventCapacityTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='Skepticamp NYC 2025',
            date=date(2025, 12, 6),
            start_time=time(9, 30),
            end_time=time(18, 0),
            venue_name='Test Venue',
            venue_address='123 Test St',
            venue_city='New York, NY',
            is_active=True,
            max_capacity=2,
        )

    def test_under_capacity_returns_false(self):
        Registration.objects.create(
            registration_type='attendee',
            status='confirmed',
            first_name='A',
            last_name='B',
            email='a@example.com',
            gdpr_consent=True,
            code_of_conduct_accepted=True,
        )
        self.assertFalse(self.event.is_at_capacity)

    def test_at_capacity_returns_true(self):
        for i in range(2):
            Registration.objects.create(
                registration_type='attendee',
                status='confirmed',
                first_name='User',
                last_name=str(i),
                email=f'user{i}@example.com',
                gdpr_consent=True,
                code_of_conduct_accepted=True,
            )
        self.assertTrue(self.event.is_at_capacity)

    def test_no_max_capacity_never_at_capacity(self):
        self.event.max_capacity = None
        self.event.save()
        self.assertFalse(self.event.is_at_capacity)


class EventVenueAddressTest(TestCase):
    def test_full_venue_address_formatting(self):
        event = Event.objects.create(
            name='Test Event',
            date=date(2025, 12, 6),
            start_time=time(9, 30),
            end_time=time(18, 0),
            venue_name='Hall',
            venue_address='123 Main St',
            venue_city='New York, NY',
        )
        self.assertEqual(event.full_venue_address, '123 Main St, New York, NY')


class EventActiveFilterTest(TestCase):
    def test_is_active_filtering(self):
        # Deactivate any seeded events from migrations
        Event.objects.update(is_active=False)

        Event.objects.create(
            name='Active Event',
            date=date(2025, 12, 6),
            start_time=time(9, 30),
            end_time=time(18, 0),
            venue_name='V',
            venue_address='A',
            venue_city='C',
            is_active=True,
        )
        Event.objects.create(
            name='Inactive Event',
            date=date(2024, 12, 6),
            start_time=time(9, 30),
            end_time=time(18, 0),
            venue_name='V',
            venue_address='A',
            venue_city='C',
            is_active=False,
        )
        active = Event.objects.filter(is_active=True)
        self.assertEqual(active.count(), 1)
        self.assertEqual(active.first().name, 'Active Event')
