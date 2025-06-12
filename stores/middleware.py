from .models import Store

class StoreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Simple implementation - in a real app, you might determine the store
        # based on subdomain, URL path, or user session
        request.current_store = None
        
        # For demo purposes, try to get the first store
        if request.user.is_authenticated:
            try:
                request.current_store = Store.objects.filter(owner=request.user).first()
            except:
                pass
        
        response = self.get_response(request)
        return response