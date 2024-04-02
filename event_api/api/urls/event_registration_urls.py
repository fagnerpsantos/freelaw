from django.urls import path, include
from rest_framework import routers
from ..views.event_registration_views import EventRegistrationView



urlpatterns = [
    path('', EventRegistrationView.as_view(), name='event-registration-list'),
]