import json
from django.core.cache import cache
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from server import load_clients


class ClientConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'client_list_group'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        pass

    def send_clients_info(self, event):
        clients = load_clients()
        formatted_clients = {
            client_id: {
                "address": clients[client_id]["address"],
                "username": clients[client_id]["username"],
                "os": clients[client_id]["os"]
            }
            for client_id in clients
        }
        self.send(text_data=json.dumps({'agents': formatted_clients}))


class CommandConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'command_responses_group'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        pass

    def send_command_responses(self, event):
        command_responses = cache.get('command_responses', {})
        self.send(text_data=json.dumps({'command_responses': command_responses}))