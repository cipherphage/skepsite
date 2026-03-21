"""
Server-side forms for the registration app.
The primary registration flow uses the Vue wizard + JSON API,
but these forms provide a fallback for server-side validation reference.
"""
from django import forms
from .models import Registration


class BaseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'how_heard', 'attendance_format', 'dietary_needs',
            'accessibility_needs', 'donation_amount',
            'gdpr_consent', 'code_of_conduct_accepted',
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        reg_type = self.initial.get('registration_type')
        if reg_type and Registration.objects.filter(email=email, registration_type=reg_type).exists():
            raise forms.ValidationError(
                f'This email is already registered as an {reg_type}.'
            )
        return email
