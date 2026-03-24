from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue_name = models.CharField(max_length=200)
    venue_address = models.CharField(max_length=500)
    venue_city = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    max_capacity = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    editing_deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Deadline after which presenters can no longer edit their presentation details.',
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.name} — {self.date}'

    @property
    def is_at_capacity(self) -> bool:
        if self.max_capacity is None:
            return False
        from apps.registration.models import Registration
        confirmed_count = Registration.objects.filter(
            status=Registration.STATUS_CONFIRMED
        ).count()
        return confirmed_count >= self.max_capacity

    @property
    def full_venue_address(self) -> str:
        return f'{self.venue_address}, {self.venue_city}'

    @property
    def is_editing_open(self) -> bool:
        """Return True if the editing deadline has not yet passed."""
        if self.editing_deadline is None:
            return True
        from django.utils import timezone
        return timezone.now() < self.editing_deadline
