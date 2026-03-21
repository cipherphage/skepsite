import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_type', models.CharField(
                    choices=[('attendee', 'Attendee'), ('presenter', 'Presenter'), ('volunteer', 'Volunteer')],
                    max_length=20,
                )),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('confirmed', 'Confirmed'),
                        ('waitlisted', 'Waitlisted'),
                        ('cancelled', 'Cancelled'),
                    ],
                    default='confirmed',
                    max_length=20,
                )),
                ('confirmation_token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('confirmation_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField()),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('how_heard', models.CharField(blank=True, max_length=50)),
                ('attendance_format', models.CharField(
                    blank=True,
                    choices=[('in_person', 'In Person'), ('online', 'Online')],
                    max_length=20,
                )),
                ('dietary_needs', models.JSONField(blank=True, default=list)),
                ('accessibility_needs', models.TextField(blank=True)),
                ('talk_title', models.CharField(blank=True, max_length=200)),
                ('talk_duration', models.CharField(blank=True, max_length=5)),
                ('talk_description', models.TextField(blank=True)),
                ('audience_level', models.CharField(blank=True, max_length=30)),
                ('bio', models.TextField(blank=True)),
                ('affiliation', models.CharField(blank=True, max_length=100)),
                ('presented_before', models.BooleanField(blank=True, null=True)),
                ('av_needs', models.JSONField(blank=True, default=list)),
                ('remote_presenting', models.BooleanField(blank=True, null=True)),
                ('preferred_session_time', models.CharField(blank=True, max_length=30)),
                ('volunteer_roles', models.JSONField(blank=True, default=list)),
                ('volunteer_notes', models.TextField(blank=True)),
                ('volunteer_availability', models.CharField(blank=True, max_length=20)),
                ('volunteer_shift_details', models.TextField(blank=True)),
                ('donation_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('gdpr_consent', models.BooleanField(default=False)),
                ('code_of_conduct_accepted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='registration',
            index=models.Index(fields=['email', 'registration_type'], name='reg_email_type_idx'),
        ),
        migrations.AddIndex(
            model_name='registration',
            index=models.Index(fields=['confirmation_token'], name='reg_token_idx'),
        ),
        migrations.AddIndex(
            model_name='registration',
            index=models.Index(fields=['confirmation_number'], name='reg_conf_num_idx'),
        ),
    ]
