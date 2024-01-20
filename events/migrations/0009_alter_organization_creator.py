# Generated by Django 5.0.1 on 2024-01-18 16:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_customuser_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]