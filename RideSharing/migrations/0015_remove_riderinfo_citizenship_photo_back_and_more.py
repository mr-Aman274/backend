# Generated by Django 4.1.6 on 2023-03-16 05:05

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideSharing', '0014_rename_vehicleinformation_vehicleinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riderinfo',
            name='citizenship_photo_back',
        ),
        migrations.RemoveField(
            model_name='riderinfo',
            name='citizenship_photo_front',
        ),
        migrations.RemoveField(
            model_name='riderinfo',
            name='id_confirmation_photo',
        ),
        migrations.RemoveField(
            model_name='vehicleinfo',
            name='license_photo',
        ),
        migrations.RemoveField(
            model_name='vehicleinfo',
            name='vehicle_photo',
        ),
        migrations.AddField(
            model_name='riderinfo',
            name='citizenship_image_back',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='citizenship_image_back'),
        ),
        migrations.AddField(
            model_name='riderinfo',
            name='citizenship_image_front',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='citizenshipPictures'),
        ),
        migrations.AddField(
            model_name='riderinfo',
            name='id_confirmation_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='idConfirmationPictures'),
        ),
        migrations.AddField(
            model_name='vehicleinfo',
            name='license_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='LicensePictures'),
        ),
        migrations.AddField(
            model_name='vehicleinfo',
            name='vehicle_buy_year',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='vehicleinfo',
            name='vehicle_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='vehiclePictures'),
        ),
        migrations.AlterField(
            model_name='riderinfo',
            name='citizenship_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='current_address',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='dob',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='first_name',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_profile',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='user_profile'),
        ),
        migrations.AlterField(
            model_name='vehicleinfo',
            name='billbook_page2',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='billbookPictures'),
        ),
        migrations.AlterField(
            model_name='vehicleinfo',
            name='billbook_page3',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='billbookPictures'),
        ),
        migrations.AlterField(
            model_name='vehicleinfo',
            name='billbook_page9',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='billbookPictures'),
        ),
    ]
