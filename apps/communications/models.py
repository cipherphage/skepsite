from django.db import models


class EmailLog(models.Model):
    registration = models.ForeignKey(
        'registration.Registration',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_logs',
    )
    to_email = models.EmailField()
    subject = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        status = 'sent' if self.success else 'failed'
        return f'[{status}] {self.subject} → {self.to_email}'
