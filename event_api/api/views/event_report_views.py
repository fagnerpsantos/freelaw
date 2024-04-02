import csv

from django.db.models import Count
from django.http import HttpResponse
from rest_framework.views import APIView

from ..models.event_registration_models import EventRegistration
from ..models.event_models import Event


class EventReportViewSet(APIView):

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.DictWriter(response, fieldnames=['event_name', 'qtd_participants', 'event_date'])
        writer.writeheader()
        events = Event.objects.all()
        for event in events:
            participants = EventRegistration.objects.filter(event=event).aggregate(participants_count=Count('user'))["participants_count"]
            writer.writerow({'event_name': event.name, 'qtd_participants': participants, 'event_date': event.date})
        return response