# Generated by Django 5.0.1 on 2024-01-18 16:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_organization_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='organization',
            name='creator',
            field=models.ForeignKey(blank=True, help_text='If empty, then creator is authenticated user', on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
