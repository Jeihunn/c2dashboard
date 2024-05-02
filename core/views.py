from django.shortcuts import render, redirect
from subprocess import Popen
from server import HOST, PORT, load_clients, remove_all_clients
from django.contrib import messages
import psutil
import socket


# Global variable
server_process = None


def start_server(request):
    global server_process
    clients = load_clients()
    formatted_clients = {
        client_id: {
            "address": clients[client_id]["address"],
            "username": clients[client_id]["username"],
            "os": clients[client_id]["os"]
        }
        for client_id in clients
    }
    connected_agents = formatted_clients  # Get the list of connected clients
    if request.method == 'POST':
        try:
            global server_process
            # Start your server
            server_process = Popen(['python', 'server.py'])
            messages.success(request, f'Server listening on {HOST}:{PORT}')

        except Exception as e:
            messages.error(request, f'Error starting server: {e}')
    context = {
        'connected_agents': connected_agents,
        'server_process': server_process
    }
    return render(request, 'index.html', context)


def stop_server(request):
    global server_process
    if server_process is not None:
        # Find the process associated with the server
        for proc in psutil.process_iter(['pid', 'name']):
            if 'python' in proc.info['name'] and 'server.py' in proc.cmdline():
                proc.terminate()
                server_process = None
                messages.success(request, 'Server stopped successfully')
                print('Server stopped successfully')
                break
        else:
            server_process = None
            messages.error(request, 'Server process not found')
            print('Server process not found')
    else:
        server_process = None
        messages.error(request, 'Server is not running')
        print('Server is not running')
    remove_all_clients()
    return redirect('start_server')


import json


def generate_active_sockets():
    active_sockets = {}
    with open('connected_clients.json', 'r') as json_file:
        clients = json.load(json_file)
        for client_id, client_info in clients.items():
            if 'socket' in client_info:  # Check if client_info contains socket information
                try:
                    # Retrieve the existing socket from client_info and add it to active_sockets
                    active_sockets[client_id] = client_info['socket']
                except Exception as e:
                    print(f'Error retrieving socket for {client_info["username"]}: {e}')
            else:
                print(f'No socket information found for {client_info["username"]}')
    return active_sockets


# from server import client_sockets, count
from client import client_socket
from core.tests import count

def send_command(request):
    print('Client sockets send command', client_socket)
    print('Count', count)

    return redirect('start_server')





# def send_command(request):
#     if request.method == 'POST':
#         command = request.POST.get('command', '')
#         print(type(command))
#         if not command:
#             messages.error(request, 'Command cannot be empty')
#             return redirect('start_server')

#         clients = load_clients()

#         for client_id, client_info in clients.items():
#             try:
#                 client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 client_socket.settimeout(5)  # Setting a timeout for connection and response
                
#                 client_address = (client_info["address"][0], int(client_info["address"][1]))
#                 client_socket.connect(client_address)
#                 client_socket.send(command.encode())

#                 # Here you could add code to receive a response
#                 # response = client_socket.recv(4096).decode()
#                 # print(f'Response from {client_info["username"]}: {response}')

#                 client_socket.close()
#                 messages.success(request, f'Command "{command}" sent to {client_info["username"]}')
#             except socket.timeout:
#                 messages.error(request, f'Timeout when connecting to {client_info["username"]}')
#             except Exception as e:
#                 messages.error(request, f'Error sending command to {client_info["username"]}: {e}')
#             finally:
#                 client_socket.close()  # Ensure the socket is closed even if an error occurs

#     return redirect('start_server')