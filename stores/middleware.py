from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Store

class StoreMiddleware:
    """Middleware to handle subdomain routing for stores"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract subdomain from host
        host = request.get_host().split(':')[0]  # Remove port if present
        host_parts = host.split('.')
        
        # Check if this is a subdomain request
        if len(host_parts) > 2 and host_parts[0] != 'www':
            subdomain = host_parts[0]
            try:
                store = Store.objects.get(subdomain=subdomain, is_published=True)
                request.store = store
            except Store.DoesNotExist:
                request.store = None
        else:
            request.store = None
        
        response = self.get_response(request)
        return response