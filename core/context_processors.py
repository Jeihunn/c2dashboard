
from django.core.cache import cache

def command_responses_context(request):
    command_responses = cache.get('command_responses', {})
    return {'command_responses': command_responses}