import base64
import time

from django.apps import apps
from django.core.files.base import ContentFile

from celery import Celery, shared_task

app = Celery('tasks', broker='redis://localhost:6379//')


@shared_task
def sleep_60_when_create_event(data):
    time.sleep(60)
    organization_model = apps.get_model(app_label='events', model_name='Organization')
    event_model = apps.get_model(app_label='events', model_name='Event')
    organizers = organization_model.objects.filter(id__in=data.pop('organizers'))
    image_content = base64.b64decode(data.pop('image'))
    image_name = data.pop('image_name')
    event = event_model.objects.create(**data)
    event.image.save(image_name, ContentFile(image_content), save=True)
    event.organizers.set(organizers)
    event.save()
