from unittest.mock import patch

from django.test import TestCase

from apps.communications.models import EmailLog
from apps.communications.email_utils import send_registration_confirmation, send_contact_message
from apps.registration.models import Registration


class EmailLogModelTest(TestCase):
    def test_create_email_log(self):
        log = EmailLog.objects.create(
            to_email='test@example.com',
            subject='Test Subject',
            success=True,
        )
        self.assertEqual(log.to_email, 'test@example.com')
        self.assertTrue(log.success)

    def test_email_log_str_sent(self):
        log = EmailLog.objects.create(
            to_email='test@example.com',
            subject='Test Subject',
            success=True,
        )
        self.assertIn('sent', str(log))

    def test_email_log_str_failed(self):
        log = EmailLog.objects.create(
            to_email='test@example.com',
            subject='Test Subject',
            success=False,
            error_message='Connection refused',
        )
        self.assertIn('failed', str(log))


class SendRegistrationConfirmationTest(TestCase):
    def setUp(self):
        self.registration = Registration.objects.create(
            registration_type='attendee',
            first_name='Ada',
            last_name='Lovelace',
            email='ada@example.com',
            gdpr_consent=True,
            code_of_conduct_accepted=True,
        )

    @patch('apps.communications.email_utils.send_mail')
    def test_sends_email_successfully(self, mock_send_mail):
        result = send_registration_confirmation(self.registration)
        self.assertTrue(result)
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args
        self.assertIn(self.registration.confirmation_number, call_kwargs[1]['subject'])
        self.assertEqual(call_kwargs[1]['recipient_list'], ['ada@example.com'])

    @patch('apps.communications.email_utils.send_mail')
    def test_creates_email_log_on_success(self, mock_send_mail):
        send_registration_confirmation(self.registration)
        log = EmailLog.objects.first()
        self.assertIsNotNone(log)
        self.assertTrue(log.success)
        self.assertEqual(log.to_email, 'ada@example.com')

    @patch('apps.communications.email_utils.send_mail', side_effect=Exception('SMTP error'))
    def test_handles_send_failure_gracefully(self, mock_send_mail):
        result = send_registration_confirmation(self.registration)
        self.assertFalse(result)
        log = EmailLog.objects.first()
        self.assertFalse(log.success)
        self.assertIn('SMTP error', log.error_message)


class SendContactMessageTest(TestCase):
    @patch('apps.communications.email_utils.send_mail')
    def test_sends_contact_message_successfully(self, mock_send_mail):
        result = send_contact_message(
            name='Jane Doe',
            email='jane@example.com',
            subject='Question',
            message='Hello, I have a question.',
        )
        self.assertTrue(result)
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args[1]
        self.assertIn('[Skepticamp Contact]', call_kwargs['subject'])
        self.assertIn('jane@example.com', call_kwargs['reply_to'])

    @patch('apps.communications.email_utils.send_mail')
    def test_creates_email_log_for_contact(self, mock_send_mail):
        send_contact_message(
            name='Jane',
            email='jane@example.com',
            subject='Hi',
            message='Hello',
        )
        log = EmailLog.objects.first()
        self.assertIsNotNone(log)
        self.assertTrue(log.success)
        self.assertIsNone(log.registration)

    @patch('apps.communications.email_utils.send_mail', side_effect=Exception('Timeout'))
    def test_handles_contact_send_failure(self, mock_send_mail):
        result = send_contact_message(
            name='Jane',
            email='jane@example.com',
            subject='Hi',
            message='Hello',
        )
        self.assertFalse(result)
        log = EmailLog.objects.first()
        self.assertFalse(log.success)
        self.assertIn('Timeout', log.error_message)
