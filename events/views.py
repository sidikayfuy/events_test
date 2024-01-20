import base64
from datetime import datetime

from django.shortcuts import render
from rest_framework import generics, filters, exceptions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import DateField
from django.db.models.functions import Cast
from rest_framework.response import Response
from .tasks import sleep_60_when_create_event
from events.models import Organization, Event
from events.serializers import CustomUserSerializer, OrganizationUserSerializer, OrganizationAdminSerializer, \
    EventSerializer, EventWithMembersSerializer


class UsersView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


class OrganizationView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return OrganizationAdminSerializer
        else:
            return OrganizationUserSerializer


class EventsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['message'] = 'Event will be added after 60 seconds'
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        image_field = serializer.validated_data['image']
        image_content = base64.b64encode(image_field.read()).decode('utf-8') if image_field else None
        data = {
            'title': serializer.validated_data['title'],
            'description': serializer.validated_data['description'],
            'organizers': [i.id for i in serializer.validated_data['organizers']],
            'image': image_content,
            'image_name': image_field.name,
            'date': serializer.validated_data['date'],
        }

        sleep_60_when_create_event.delay(data)


class EventsByOrganizationsView(generics.ListAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EventWithMembersSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class EventsListView(generics.ListAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['date']
    search_fields = ['title']

    def get_queryset(self):
        queryset = Event.objects.all()

        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        need_date = self.request.query_params.get('need_date', None)

        if (from_date or to_date) and need_date:
            error_message = "Cannot use 'need_date' with 'from_date' or 'to_date'."
            raise exceptions.ValidationError({"error": error_message})

        if from_date and to_date:
            queryset = queryset.filter(date__range=(from_date, to_date))
        elif from_date:
            queryset = queryset.filter(date__gte=from_date)
        elif to_date:
            queryset = queryset.filter(date__lte=to_date)

        if need_date:
            need_date_datetime = datetime.strptime(need_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0,
                                                                                  microsecond=0)
            queryset = queryset.annotate(date_only=Cast('date', output_field=DateField()))
            queryset = queryset.filter(date_only=need_date_datetime.date())

        return queryset


def chat(request):
    return render(request, 'events/chat.html')

