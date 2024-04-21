from django.urls import path
from .views import start_server, stop_server, send_command

urlpatterns = [
    path('', start_server, name='start_server'),
    path('stop-server/', stop_server, name='stop_server'),
    path('send-command/', send_command, name='send_command'),
]
