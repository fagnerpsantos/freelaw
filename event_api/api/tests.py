import csv
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.http import HttpResponse

from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save, post_delete, pre_delete

from .models import Event, EventRegistration
from .views.event_report_views import EventReportViewSet


class EventCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event_data = {
            'name': 'Test Event',
            'description': 'This is a test event',
            'date': '2024-04-01',
            'time': '12:00:00',
            'location': 'Test Location'
        }
        self.event = Event.objects.create(**self.event_data)

    def test_create_event(self):
        url = reverse('event-list')
        response = self.client.post(url, self.event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_events(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.event.name)

    def test_create_event_error(self):
        url = reverse('event-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_event(self):
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.event.name)

    def test_update_event(self):
        updated_data = {
            'name': 'Updated Event Name',
            'description': 'This is an updated event description',
            'date': '2024-04-02',
            'time': '13:00:00',
            'location': 'Updated Location'
        }
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, updated_data['name'])
        self.assertEqual(self.event.description, updated_data['description'])
        self.assertEqual(str(self.event.date), updated_data['date'])
        self.assertEqual(str(self.event.time), updated_data['time'])
        self.assertEqual(self.event.location, updated_data['location'])

    def test_delete_event(self):
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'b5X9t@example.com',
            'password': 'testpassword'
        }

    def test_user_registration(self):
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_error(self):
        url = reverse('user-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class TokenCreationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

    def test_token_creation(self):
        url = '/token/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        url = '/token/refresh/'
        refresh = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_refresh_error(self):
        url = '/token/refresh/'
        data = {'refresh': 'invalid'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventRegistrationTestCase(TestCase):
    def setUp(self):
        post_save.disconnect()
        post_delete.disconnect()
        pre_delete.disconnect()

        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.event = Event.objects.create(name='Test Event', description='Description', date='2024-04-01', time='12:00:00', location='Test Location')
        self.event_registration_data = {
            'user': self.user.pk,
            'event': self.event.pk
        }
        self.event_registration = EventRegistration.objects.create(user=self.user, event=self.event)

    def test_create_event_registration(self):
        with patch('api.tasks.send_email_tasks.send_registration_email.delay') as mock_send_mail:
            url = reverse('event-registration-list')
            self.client.force_authenticate(user=self.user)
            response = self.client.post(url, self.event_registration_data, format='json')
            mock_send_mail.assert_called_once()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_event_registration(self):
        url = reverse('event-registration-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_create_event_registration_without_authentication(self):
        url = reverse('event-registration-list')
        response = self.client.post(url, self.event_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReportViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('api.models.event_models.Event.objects.all')
    @patch('api.models.event_registration_models.EventRegistration.objects.filter')
    def test_get_endpoint_returns_csv(self, mock_event_reg_filter, mock_events_all):
        mock_event = MagicMock()
        mock_event.name = "Event 1"
        mock_event.date = "2024-04-02"
        mock_events_all.return_value = [mock_event]

        mock_reg_aggregate = MagicMock()
        mock_reg_aggregate.participants_count = 10
        mock_event_reg_filter.return_value.aggregate.return_value = mock_reg_aggregate

        request = self.factory.get('/your-endpoint-url/')
        response = EventReportViewSet().get(request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.get('Content-Type'), 'text/csv')

    @patch('api.models.event_models.Event.objects.all')
    @patch('api.models.event_registration_models.EventRegistration.objects.filter')
    def test_csv_contains_expected_data(self, mock_event_reg_filter, mock_events_all):
        mock_event = MagicMock()
        mock_event.name = "Event 1"
        mock_event.date = "2024-04-02"
        mock_events_all.return_value = [mock_event]

        mock_reg_aggregate = MagicMock()
        mock_reg_aggregate.participants_count = 10
        mock_event_reg_filter.return_value.aggregate.return_value = mock_reg_aggregate

        request = self.factory.get('/your-endpoint-url/')
        response = EventReportViewSet().get(request)

        decoded_response = response.content.decode('utf-8')
        csv_reader = csv.DictReader(decoded_response.splitlines())

        rows = list(csv_reader)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['event_name'], 'Event 1')
        self.assertEqual(rows[0]['event_date'], '2024-04-02')

