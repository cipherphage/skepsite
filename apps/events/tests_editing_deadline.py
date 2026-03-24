"""
Tests for the Event.is_editing_open property.
"""
from datetime import date, time, timedelta

from django.test import TestCase
from django.utils import timezone

from apps.events.models import Event


class EditingDeadlineTest(TestCase):
    def _create_event(self, **overrides):
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

    def test_editing_open_when_deadline_is_none(self):
        event = self._create_event(editing_deadline=None)
        self.assertTrue(event.is_editing_open)

    def test_editing_open_when_deadline_is_in_future(self):
        event = self._create_event(
            editing_deadline=timezone.now() + timedelta(days=7),
        )
        self.assertTrue(event.is_editing_open)

    def test_editing_closed_when_deadline_is_in_past(self):
        event = self._create_event(
            editing_deadline=timezone.now() - timedelta(hours=1),
        )
        self.assertFalse(event.is_editing_open)

    def test_editing_closed_when_deadline_just_passed(self):
        event = self._create_event(
            editing_deadline=timezone.now() - timedelta(seconds=1),
        )
        self.assertFalse(event.is_editing_open)
