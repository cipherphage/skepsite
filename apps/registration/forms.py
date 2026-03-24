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


class RegistrantLoginForm(forms.Form):
    """Login form for registered users using email + confirmation number."""
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'you@example.com',
            'autocomplete': 'email',
            'required': True,
        }),
    )
    confirmation_number = forms.CharField(
        label='Confirmation number',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. SKC-2025-A-00001',
            'autocomplete': 'off',
            'required': True,
        }),
    )

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_confirmation_number(self):
        return self.cleaned_data['confirmation_number'].strip().upper()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirmation_number = cleaned_data.get('confirmation_number')

        if email and confirmation_number:
            try:
                registration = Registration.objects.get(
                    email=email,
                    confirmation_number=confirmation_number,
                )
                cleaned_data['registration'] = registration
            except Registration.DoesNotExist:
                raise forms.ValidationError(
                    'No registration found with that email and confirmation number. '
                    'Please check your details and try again.'
                )
        return cleaned_data


class PresentationEditForm(forms.ModelForm):
    """Form for presenters to edit their presentation details."""
    class Meta:
        model = Registration
        fields = [
            'talk_title', 'talk_description', 'talk_duration',
            'audience_level', 'av_needs', 'bio', 'affiliation',
        ]
        widgets = {
            'talk_title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your talk title',
            }),
            'talk_description': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Describe your talk...',
                'rows': 5,
            }),
            'talk_duration': forms.Select(
                choices=[('', 'Select duration'), ('15', '15 minutes'), ('30', '30 minutes')],
                attrs={'class': 'form-input'},
            ),
            'audience_level': forms.Select(
                choices=[
                    ('', 'Select level'),
                    ('beginner', 'Beginner'),
                    ('intermediate', 'Intermediate'),
                    ('advanced', 'Advanced'),
                    ('all', 'All levels'),
                ],
                attrs={'class': 'form-input'},
            ),
            'bio': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'A brief bio about yourself...',
                'rows': 3,
            }),
            'affiliation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Organization, university, etc.',
            }),
        }
        labels = {
            'talk_title': 'Talk title',
            'talk_description': 'Talk description',
            'talk_duration': 'Duration',
            'audience_level': 'Audience level',
            'av_needs': 'A/V needs',
            'bio': 'Bio',
            'affiliation': 'Affiliation',
        }

    def clean_talk_title(self):
        title = self.cleaned_data.get('talk_title', '').strip()
        if not title:
            raise forms.ValidationError('Talk title is required.')
        return title
