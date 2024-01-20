from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('users/', views.UsersView.as_view()),
    path('organizations/', views.OrganizationView.as_view()),
    path('events/', views.EventsView.as_view()),
    path('eventsByOrganizations/', views.EventsByOrganizationsView.as_view()),
    path('eventsList/', views.EventsListView.as_view()),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls')),
    path('', views.chat, name='index')
]
