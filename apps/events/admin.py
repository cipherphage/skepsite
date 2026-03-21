from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue_name', 'is_active', 'max_capacity')
    list_filter = ('is_active',)
    search_fields = ('name', 'venue_name')
