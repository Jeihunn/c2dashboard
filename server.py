import socket
import threading
import json

HOST = "0.0.0.0"  # Set your host
PORT = 8888  # Set your port

# Dosya adı
CLIENTS_FILE = "connected_clients.json"


def load_clients():
    try:
        with open(CLIENTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_clients(clients):
    with open(CLIENTS_FILE, "w") as file:
        json.dump(clients, file)


def add_client(client_id, client_socket):
    clients = load_clients()
    clients[client_id] = {"socket": client_socket.fileno(
    ), "address": client_socket.getpeername()}
    save_clients(clients)
    print(f"Connected agents: {list_clients()}")


def remove_client(client_id):
    clients = load_clients()
    if client_id in clients:
        del clients[client_id]
        save_clients(clients)
        print(f"Connected agents: {list_clients()}")


def remove_all_clients():
    clients = load_clients()
    clients.clear()
    save_clients(clients)
    print(f"Connected agents: {list_clients()}")


def list_clients():
    clients = load_clients()
    return list(clients.keys())


class AgentHandler(threading.Thread):
    def __init__(self, agent_socket, agent_address):
        super().__init__()
        self.agent_socket = agent_socket
        self.agent_address = agent_address
        # Unique identifier for each client
        self.agent_id = f"{agent_address[0]}:{agent_address[1]}"

    def run(self):
        print(f"New agent connected: {self.agent_address}")
        try:
            while True:
                command = input(
                    "Enter command to send to agent (type 'exit' to disconnect): ").strip()
                if not command:
                    continue
                self.agent_socket.send(command.encode())
                if command.lower() == "exit":
                    break
                response = self.agent_socket.recv(4096).decode()
                print(f"Response from agent {self.agent_address}:")
                print(response)
        except Exception as e:
            print(f"Error communicating with agent {self.agent_address}: {e}")
        finally:
            self.agent_socket.close()
            print(f"Agent {self.agent_address} disconnected")
            # Remove the client from the list when disconnected
            remove_client(self.agent_id)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            agent_socket, agent_address = server_socket.accept()
            agent_handler = AgentHandler(agent_socket, agent_address)
            agent_handler.start()
            # Add the client to the list
            add_client(agent_handler.agent_id, agent_socket)
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
