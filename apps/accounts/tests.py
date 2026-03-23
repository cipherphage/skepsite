from django.test import TestCase, Client

from apps.accounts.models import User


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123',
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('securepassword123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.mfa_enabled)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str_returns_email_or_username(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass',
        )
        # __str__ returns email if set
        self.assertEqual(str(user), 'test@example.com')

    def test_user_str_falls_back_to_username(self):
        user = User.objects.create_user(
            username='testuser',
            email='',
            password='pass',
        )
        self.assertEqual(str(user), 'testuser')


class AdminLoginPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_admin_login_page_returns_200(self):
        response = self.client.get('/admin-login/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login_with_invalid_credentials_shows_error(self):
        response = self.client.post('/admin-login/', {
            'username': 'nonexistent',
            'password': 'wrongpassword',
            'totp_token': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_admin_login_non_staff_user_denied(self):
        User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='pass123',
            is_staff=False,
        )
        response = self.client.post('/admin-login/', {
            'username': 'regular',
            'password': 'pass123',
            'totp_token': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'do not have permission')
