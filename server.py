import socket
import threading

HOST = "0.0.0.0"  # Set your host
PORT = 8888  # Set your port

class AgentHandler(threading.Thread):
    def __init__(self, agent_socket, agent_address):
        super().__init__()
        self.agent_socket = agent_socket
        self.agent_address = agent_address

    def run(self):
        print(f"New agent connected: {self.agent_address}")
        try:
            while True:
                command = input("Enter command to send to agent (type 'exit' to disconnect): ").strip()
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
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
