from django.urls import path, include
from rest_framework import routers
from ..views.event_views import EventListView, EventDetailView



urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
]