# Generated by Django 5.0.1 on 2024-01-19 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_rename_organizations_event_organizers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
