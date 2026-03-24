from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue_name', 'is_active', 'max_capacity', 'editing_deadline')
    list_filter = ('is_active',)
    search_fields = ('name', 'venue_name')
    fieldsets = (
        (None, {
            'fields': ('name', 'date', 'start_time', 'end_time', 'is_active', 'max_capacity', 'description'),
        }),
        ('Venue', {
            'fields': ('venue_name', 'venue_address', 'venue_city'),
        }),
        ('Presenter Editing', {
            'fields': ('editing_deadline',),
            'description': 'Set a deadline after which presenters can no longer edit their presentation details.',
        }),
    )
