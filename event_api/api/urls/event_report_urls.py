from django.urls import path, include
from rest_framework import routers
from ..views.event_report_views import EventReportViewSet



urlpatterns = [
    path('', EventReportViewSet.as_view(), name='event-report-list'),
]