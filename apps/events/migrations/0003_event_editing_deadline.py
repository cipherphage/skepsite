from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_initial_event_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='editing_deadline',
            field=models.DateTimeField(
                blank=True,
                help_text='Deadline after which presenters can no longer edit their presentation details.',
                null=True,
            ),
        ),
    ]
