from django.shortcuts import render
from rest_framework import mixins, status, renderers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.event_registration_models import EventRegistration
from ..serializers.event_serializers import EventRegistrationSerializer


class EventRegistrationView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)