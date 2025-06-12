from django.http import HttpResponseRedirect
from django.conf import settings
import re

class SecurityMiddleware:
    """Middleware to enforce security headers and HTTPS"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Enforce HTTPS in production
        if not settings.DEBUG and not request.is_secure():
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace('http://', 'https://')
            return HttpResponseRedirect(secure_url)
            
        response = self.get_response(request)
        
        # Add security headers
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline'; "  # Allow inline styles for theme customization
            "script-src 'self' https://checkout.razorpay.com 'unsafe-inline'; "  # Allow Razorpay and inline scripts
            "connect-src 'self' https://checkout.razorpay.com; "
            "frame-src 'self' https://checkout.razorpay.com; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
        )
        response['Content-Security-Policy'] = csp
        
        return response

class StoreThemeMiddleware:
    """Middleware to load store theme based on URL"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Check if URL matches store pattern
        store_pattern = r'^/stores/store/([^/]+)/'
        match = re.match(store_pattern, request.path)
        
        if match:
            from stores.models import Store
            store_slug = match.group(1)
            try:
                store = Store.objects.get(slug=store_slug)
                # Add store theme to request for template context
                request.current_store = store
            except Store.DoesNotExist:
                pass
                
        response = self.get_response(request)
        return response