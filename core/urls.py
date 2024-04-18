from django.urls import path
from .views import start_server

urlpatterns = [
    path('', start_server, name='start_server'),
]
