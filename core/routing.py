from django.urls import path
from .consumers import ClientConsumer

websocket_urlpatterns = [
    path('ws/clients/', ClientConsumer.as_asgi()),
]
