# Generated by Django 4.2 on 2023-04-27 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideSharing', '0017_rideinfo_date_rideinfo_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='dob',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]