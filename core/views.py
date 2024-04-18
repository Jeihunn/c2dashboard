from django.shortcuts import render
from django.http import JsonResponse
from subprocess import Popen, PIPE
from server import HOST, PORT
from django.contrib import messages
import time

def start_server(request):
    if request.method == 'POST':
        try:
            # Start your server
            Popen(['python3', 'server.py'])  
            messages.success(request, f'Server listening on {HOST}:{PORT}')
        except Exception as e:
            messages.error(request, f'Error starting server: {e}')
    return render(request, 'index.html')

