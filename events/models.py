from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from events.managers import CustomUserManager
from .tasks import sleep_60_when_create_event


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Organization(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150)
    postcode = models.CharField(max_length=6)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='creator', blank=True)
    members = models.ManyToManyField(CustomUser, related_name='members', blank=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    organizers = models.ManyToManyField(Organization)
    image = models.ImageField(upload_to='images/', null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title




