from django.urls import path, include
from rest_framework import routers
from ..views.user_views import UserListView, UserDetailView



urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]