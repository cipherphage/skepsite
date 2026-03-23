from django.test import TestCase, Client


class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_contains_hero_section(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="hero-headline"')

    def test_homepage_contains_registration_cards(self):
        response = self.client.get('/')
        self.assertContains(response, 'reg-card--attendee')
        self.assertContains(response, 'reg-card--presenter')
        self.assertContains(response, 'reg-card--volunteer')

    def test_homepage_contains_donation_section_mount(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="donation-callout-home"')

    def test_homepage_contains_hero_illustration(self):
        response = self.client.get('/')
        self.assertContains(response, 'hero-illustration.svg')

    def test_homepage_contains_community_illustration(self):
        response = self.client.get('/')
        self.assertContains(response, 'community-illustration.svg')

    def test_homepage_contains_skyline_illustration(self):
        response = self.client.get('/')
        self.assertContains(response, 'event-photo-illustration.svg')

    def test_homepage_contains_noscript_donation_fallback(self):
        response = self.client.get('/')
        self.assertContains(response, '<noscript>')

    def test_homepage_contains_past_years(self):
        response = self.client.get('/')
        self.assertContains(response, '2009')
        self.assertContains(response, '2024')

    def test_homepage_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'pages/home.html')


class AboutPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_returns_200(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_contains_values_section(self):
        response = self.client.get('/about/')
        self.assertContains(response, 'id="values-heading"')

    def test_about_contains_donation_section_mount(self):
        response = self.client.get('/about/')
        self.assertContains(response, 'id="donation-callout-about"')

    def test_about_contains_timeline_image(self):
        response = self.client.get('/about/')
        self.assertContains(response, 'about-history.svg')

    def test_about_contains_community_illustration(self):
        response = self.client.get('/about/')
        self.assertContains(response, 'community-illustration.svg')

    def test_about_contains_org_logo(self):
        response = self.client.get('/about/')
        self.assertContains(response, 'nyc-skeptics-logo.svg')

    def test_about_contains_noscript_donation_fallback(self):
        response = self.client.get('/about/')
        self.assertContains(response, '<noscript>')

    def test_about_uses_correct_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'pages/about.html')


class ContactPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_get_returns_200(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_contact_get_contains_form(self):
        response = self.client.get('/contact/')
        self.assertContains(response, '<form')

    def test_contact_post_valid_data_redirects(self):
        response = self.client.post('/contact/', {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'Test',
            'message': 'Hello there',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('sent=1', response.url)

    def test_contact_post_missing_name_shows_error(self):
        response = self.client.post('/contact/', {
            'name': '',
            'email': 'jane@example.com',
            'subject': 'Test',
            'message': 'Hello',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name')

    def test_contact_post_missing_email_shows_error(self):
        response = self.client.post('/contact/', {
            'name': 'Jane',
            'email': '',
            'subject': 'Test',
            'message': 'Hello',
        })
        self.assertEqual(response.status_code, 200)

    def test_contact_post_missing_message_shows_error(self):
        response = self.client.post('/contact/', {
            'name': 'Jane',
            'email': 'jane@example.com',
            'subject': 'Test',
            'message': '',
        })
        self.assertEqual(response.status_code, 200)


class PrivacyPageTest(TestCase):
    def test_privacy_returns_200(self):
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)

    def test_privacy_uses_correct_template(self):
        response = self.client.get('/privacy/')
        self.assertTemplateUsed(response, 'pages/privacy.html')
