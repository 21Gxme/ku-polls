# Generated by Django 4.2.4 on 2023-09-06 06:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 7, 6, 21, 42, 734050, tzinfo=datetime.timezone.utc), verbose_name='date ended'),
        ),
    ]
