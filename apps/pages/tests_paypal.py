"""
Tests for PayPal donation integration in rendered pages.

Verifies that the noscript fallback forms contain the correct
PayPal hosted_button_id and form action.
"""
from django.test import TestCase


PAYPAL_BUTTON_ID = '83MUR59PT8XBS'
PAYPAL_DONATE_URL = 'https://www.paypal.com/donate'


class PayPalNoscriptFallbackTest(TestCase):
    """Verify PayPal noscript donation forms are correctly rendered."""

    def test_homepage_noscript_has_paypal_button_id(self):
        response = self.client.get('/')
        content = response.content.decode()
        self.assertIn(PAYPAL_BUTTON_ID, content)

    def test_homepage_noscript_has_paypal_action_url(self):
        response = self.client.get('/')
        content = response.content.decode()
        self.assertIn(PAYPAL_DONATE_URL, content)

    def test_homepage_noscript_has_submit_button(self):
        response = self.client.get('/')
        content = response.content.decode()
        self.assertIn('Donate via PayPal', content)

    def test_about_page_noscript_has_paypal_button_id(self):
        response = self.client.get('/about/')
        content = response.content.decode()
        self.assertIn(PAYPAL_BUTTON_ID, content)

    def test_about_page_noscript_has_paypal_action_url(self):
        response = self.client.get('/about/')
        content = response.content.decode()
        self.assertIn(PAYPAL_DONATE_URL, content)

    def test_about_page_noscript_has_submit_button(self):
        response = self.client.get('/about/')
        content = response.content.decode()
        self.assertIn('Donate via PayPal', content)


class MyRegistrationNavLinkTest(TestCase):
    """Verify the 'My Registration' link appears in nav and footer."""

    def test_homepage_nav_has_my_registration_link(self):
        response = self.client.get('/')
        self.assertContains(response, '/my-registration/')

    def test_about_page_nav_has_my_registration_link(self):
        response = self.client.get('/about/')
        self.assertContains(response, '/my-registration/')
