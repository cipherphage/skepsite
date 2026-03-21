from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('venue_name', models.CharField(max_length=200)),
                ('venue_address', models.CharField(max_length=500)),
                ('venue_city', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('max_capacity', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
