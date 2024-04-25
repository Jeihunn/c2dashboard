from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from server import list_clients


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
        clients = list_clients()
        self.send(text_data=json.dumps({'agents': clients}))
