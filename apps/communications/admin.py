from django.contrib import admin
from .models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('subject', 'to_email', 'success', 'sent_at')
    list_filter = ('success',)
    search_fields = ('to_email', 'subject')
    readonly_fields = ('registration', 'to_email', 'subject', 'sent_at', 'success', 'error_message')
