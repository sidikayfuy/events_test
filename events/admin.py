import base64
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.core.files.storage import default_storage
from django.urls import reverse
from django.utils.html import format_html
from .tasks import sleep_60_when_create_event

from .models import CustomUser, Organization, Event


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ['is_staff']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'address', 'postcode', 'creator', 'members')
    list_display = ['title', 'creator']
    list_filter = ['creator', 'members']
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['creator'].initial = request.user
        return form


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'organizers', 'image', 'date')
    list_display = ['title', 'preview']
    list_filter = ['organizers', 'date']
    search_fields = ['title']

    def preview(self, obj):
        if obj.image:
            return format_html(f'<img style="height: 100px" src="{obj.image.url}" />')
        else:
            return

    def save_related(self, request, form, formsets, change):
        return

    def save_model(self, request, obj, form, change):
        image_field = form.cleaned_data['image']
        image_content = base64.b64encode(image_field.read()).decode('utf-8') if image_field else None

        data = {
            'title': form.cleaned_data['title'],
            'description': form.cleaned_data['description'],
            'organizers': list(form.cleaned_data['organizers'].values_list('id', flat=True)),
            'image': image_content,
            'image_name': image_field.name,
            'date': form.cleaned_data['date'],
        }

        sleep_60_when_create_event.delay(data)

        messages.success(request, 'Event will be added after 60 seconds.')

        return HttpResponseRedirect(reverse('admin:events_event_changelist'))

