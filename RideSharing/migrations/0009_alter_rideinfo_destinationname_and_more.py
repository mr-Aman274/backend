# Generated by Django 4.1.6 on 2023-03-07 09:33

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideSharing', '0008_rename_test_test1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rideinfo',
            name='destinationName',
            field=models.CharField(blank=True, max_length=70),
        ),
        migrations.AlterField(
            model_name='rideinfo',
            name='destinationPlaceId',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='rideinfo',
            name='originName',
            field=models.CharField(blank=True, max_length=70),
        ),
        migrations.AlterField(
            model_name='rideinfo',
            name='originPlaceId',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='rideinfo',
            name='vehicletype',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_profile',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]