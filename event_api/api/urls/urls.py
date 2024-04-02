
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("events/", include("api.urls.event_urls")),
    path("users/", include("api.urls.user_urls")),
    path("event/register/", include("api.urls.event_registration_urls")),
    path("event/report/", include("api.urls.event_report_urls")),
]
