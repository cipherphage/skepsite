from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_registration_confirmation(registration) -> bool:
    """
    Sends a confirmation email for a registration.
    Returns True on success, False on failure.
    Logs the result to EmailLog.
    """
    from .models import EmailLog

    type_label = registration.get_registration_type_display()
    subject = f'Your Skepticamp NYC Registration — {registration.confirmation_number}'

    context = {
        'registration': registration,
        'type_label': type_label,
    }

    try:
        html_body = render_to_string('communications/confirmation_email.html', context)
        text_body = render_to_string('communications/confirmation_email.txt', context)
    except Exception:
        # Fallback plain text if templates don't exist yet
        text_body = (
            f'Hi {registration.first_name},\n\n'
            f'You are registered for Skepticamp NYC 2025 as an {type_label}.\n\n'
            f'Confirmation number: {registration.confirmation_number}\n\n'
            f'Date: December 6, 2025\n'
            f'Location: 151 W. 30th St, 3rd Floor, New York, NY 10001\n\n'
            f'See you there!\n— The Skepticamp NYC Team'
        )
        html_body = None

    success = False
    error_message = ''

    try:
        send_mail(
            subject=subject,
            message=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[registration.email],
            html_message=html_body,
            fail_silently=False,
        )
        success = True
    except Exception as exc:
        error_message = str(exc)

    EmailLog.objects.create(
        registration=registration,
        to_email=registration.email,
        subject=subject,
        success=success,
        error_message=error_message,
    )

    return success


def send_contact_message(name: str, email: str, subject: str, message: str) -> bool:
    """Forwards a contact form submission to the admin email."""
    from .models import EmailLog

    full_subject = f'[Skepticamp Contact] {subject}'
    body = f'From: {name} <{email}>\n\n{message}'

    success = False
    error_message = ''

    try:
        send_mail(
            subject=full_subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            reply_to=[email],
            fail_silently=False,
        )
        success = True
    except Exception as exc:
        error_message = str(exc)

    EmailLog.objects.create(
        registration=None,
        to_email=settings.DEFAULT_FROM_EMAIL,
        subject=full_subject,
        success=success,
        error_message=error_message,
    )

    return success
