import datetime
from django.db import migrations


def create_initial_event(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    Event.objects.create(
        name='Skepticamp NYC 2025',
        date=datetime.date(2025, 12, 6),
        start_time=datetime.time(9, 30),
        end_time=datetime.time(18, 0),
        venue_name='New York City Skeptics HQ',
        venue_address='151 W. 30th St, 3rd Floor',
        venue_city='New York, NY 10001',
        is_active=True,
        max_capacity=None,
        description=(
            'Skepticamp NYC is a free, one-day unconference where curious New Yorkers '
            'present and explore science, critical thinking, and consumer protection. '
            'No credentials required — just bring your curiosity.'
        ),
    )


def remove_initial_event(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    Event.objects.filter(name='Skepticamp NYC 2025').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_event, remove_initial_event),
    ]
