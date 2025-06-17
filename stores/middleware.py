from .models import Store

class StoreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.current_store = None
        
        # Try to get store from URL path
        path_parts = request.path.strip('/').split('/')
        store_slug = None
        
        # Check if we're in a store-specific URL (e.g., /stores/store-slug/...)
        if len(path_parts) >= 2 and path_parts[0] == 'stores':
            store_slug = path_parts[1]
        
        # Check for store selection in query param
        store_query = request.GET.get('store')
        if store_query:
            store_slug = store_query
        
        # Try to get store by slug if we have one
        if store_slug:
            try:
                request.current_store = Store.objects.get(slug=store_slug)
            except Store.DoesNotExist:
                pass
        
        # For authenticated users, handle their stores
        if request.user.is_authenticated:
            # If no store found yet, check for store_id param (for store owners)
            if not request.current_store:
                selected_store_id = request.GET.get('store_id')
                
                if selected_store_id:
                    try:
                        # Try to get the selected store if user owns it
                        request.current_store = Store.objects.get(
                            id=selected_store_id, 
                            owner=request.user
                        )
                        # Save to session for persistence
                        request.session['selected_store_id'] = selected_store_id
                    except Store.DoesNotExist:
                        pass
            
            # If no store selected via query param, try session
            if not request.current_store and 'selected_store_id' in request.session:
                try:
                    request.current_store = Store.objects.get(
                        id=request.session['selected_store_id'],
                        owner=request.user
                    )
                except Store.DoesNotExist:
                    # Clear invalid store from session
                    del request.session['selected_store_id']
            
            # Fall back to first store if no selection and user is a store owner
            if not request.current_store:
                request.current_store = Store.objects.filter(owner=request.user).first()
                
            # Add user's stores to request for UI
            request.user_stores = Store.objects.filter(owner=request.user)
        
        response = self.get_response(request)
        return response