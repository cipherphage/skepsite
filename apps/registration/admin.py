from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'confirmation_number', 'full_name', 'email',
        'registration_type', 'status', 'created_at',
    )
    list_filter = ('registration_type', 'status', 'attendance_format')
    search_fields = ('first_name', 'last_name', 'email', 'confirmation_number')
    readonly_fields = ('confirmation_token', 'confirmation_number', 'created_at', 'updated_at', 'ip_address')
    ordering = ('-created_at',)

    fieldsets = (
        ('Core', {
            'fields': ('confirmation_number', 'confirmation_token', 'registration_type', 'status'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'how_heard'),
        }),
        ('Attendance', {
            'fields': ('attendance_format', 'dietary_needs', 'accessibility_needs', 'donation_amount'),
        }),
        ('Presenter Info', {
            'classes': ('collapse',),
            'fields': (
                'talk_title', 'talk_duration', 'talk_description', 'audience_level',
                'bio', 'affiliation', 'presented_before', 'av_needs',
                'remote_presenting', 'preferred_session_time',
            ),
        }),
        ('Volunteer Info', {
            'classes': ('collapse',),
            'fields': ('volunteer_roles', 'volunteer_notes', 'volunteer_availability', 'volunteer_shift_details'),
        }),
        ('Meta', {
            'fields': ('gdpr_consent', 'code_of_conduct_accepted', 'ip_address', 'created_at', 'updated_at'),
        }),
    )
