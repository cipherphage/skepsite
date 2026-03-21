import uuid
from django.db import models


class Registration(models.Model):
    # Registration types
    ATTENDEE = 'attendee'
    PRESENTER = 'presenter'
    VOLUNTEER = 'volunteer'
    TYPE_CHOICES = [
        (ATTENDEE, 'Attendee'),
        (PRESENTER, 'Presenter'),
        (VOLUNTEER, 'Volunteer'),
    ]

    # Status choices
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_WAITLISTED = 'waitlisted'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_WAITLISTED, 'Waitlisted'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    # Core fields
    registration_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CONFIRMED)
    confirmation_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    confirmation_number = models.CharField(max_length=20, unique=True, blank=True)

    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    how_heard = models.CharField(max_length=50, blank=True)

    # Attendance
    attendance_format = models.CharField(
        max_length=20,
        choices=[('in_person', 'In Person'), ('online', 'Online')],
        blank=True,
    )
    dietary_needs = models.JSONField(default=list, blank=True)
    accessibility_needs = models.TextField(blank=True)

    # Presenter-specific
    talk_title = models.CharField(max_length=200, blank=True)
    talk_duration = models.CharField(max_length=5, blank=True)  # '15' or '30'
    talk_description = models.TextField(blank=True)
    audience_level = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    affiliation = models.CharField(max_length=100, blank=True)
    presented_before = models.BooleanField(null=True, blank=True)
    av_needs = models.JSONField(default=list, blank=True)
    remote_presenting = models.BooleanField(null=True, blank=True)
    preferred_session_time = models.CharField(max_length=30, blank=True)

    # Volunteer-specific
    volunteer_roles = models.JSONField(default=list, blank=True)
    volunteer_notes = models.TextField(blank=True)
    volunteer_availability = models.CharField(max_length=20, blank=True)
    volunteer_shift_details = models.TextField(blank=True)

    # Optional donation
    donation_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    gdpr_consent = models.BooleanField(default=False)
    code_of_conduct_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'registration_type']),
            models.Index(fields=['confirmation_token']),
            models.Index(fields=['confirmation_number']),
        ]

    def __str__(self):
        return f'{self.confirmation_number} — {self.first_name} {self.last_name} ({self.registration_type})'

    def save(self, **kwargs):
        if not self.confirmation_number:
            self.confirmation_number = self._generate_confirmation_number()
        super().save(**kwargs)

    def _generate_confirmation_number(self) -> str:
        type_code = {'attendee': 'A', 'presenter': 'P', 'volunteer': 'V'}.get(
            self.registration_type, 'X'
        )
        # Use count + 1 for sequential numbering; small race condition acceptable for this use case
        count = Registration.objects.count() + 1
        return f'SKC-2025-{type_code}-{count:05d}'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('registration:confirmation', kwargs={'token': self.confirmation_token})
