from rest_framework import serializers
from django.core.mail import send_mail

from .user_serializers import UserSerializer
from ..models.event_models import Event
from ..models.event_registration_models import EventRegistration
from ..tasks.send_email_tasks import send_registration_email
class EventSerializer(serializers.ModelSerializer):
    attendees = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    event_data = serializers.SerializerMethodField('get_event_data')

    class Meta:
        model = EventRegistration
        fields = ['event', 'event_data']

    def get_event_data(self, obj):
        return EventSerializer(obj.event).data if obj.event else None


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        event_registration = super().create(validated_data)

        send_registration_email.delay(user.email, event_registration.event.name)

        return event_registration
