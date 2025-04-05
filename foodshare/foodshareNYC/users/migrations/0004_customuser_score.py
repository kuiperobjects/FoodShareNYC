# Generated by Django 3.1.6 on 2021-07-06 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='score',
            field=models.FloatField(choices=[(1.0, '*'), (2.0, '**'), (3.0, '***'), (4.0, '****'), (5.0, '*****')], default=0.0),
        ),
    ]
