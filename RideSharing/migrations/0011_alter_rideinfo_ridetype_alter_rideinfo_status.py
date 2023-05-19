# Generated by Django 4.1.6 on 2023-03-12 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideSharing', '0010_rideinfo_ridetype_alter_rideinfo_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rideinfo',
            name='rideType',
            field=models.CharField(blank=True, default='ongoing', max_length=5),
        ),
        migrations.AlterField(
            model_name='rideinfo',
            name='status',
            field=models.CharField(blank=True, choices=[('complete', 'complete'), ('cancelled', 'cancelled'), ('ongoing', 'ongoing')], max_length=10),
        ),
    ]