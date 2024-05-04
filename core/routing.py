from django.urls import path
from .consumers import ClientConsumer, CommandConsumer

websocket_urlpatterns = [
    path('ws/clients/', ClientConsumer.as_asgi()),
    path('ws/command-responses/', CommandConsumer.as_asgi()),
]
