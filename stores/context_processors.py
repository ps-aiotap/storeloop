from .models import Store

def store_theme(request):
    """
    Context processor to add store theme to template context
    """
    context = {}
    
    # Get current store from request (set by StoreMiddleware)
    current_store = getattr(request, 'current_store', None)
    
    if current_store:
        # Get theme settings with inheritance from base theme
        theme_settings = current_store.get_theme_settings()
        context['store_theme'] = theme_settings
    else:
        # Try to derive store from URL if not already set
        store_slug = None
        path_parts = request.path.strip('/').split('/')
        
        # Check if we're in a store-specific URL
        if len(path_parts) >= 2 and path_parts[0] == 'stores':
            store_slug = path_parts[1]
        
        # Check query param
        if not store_slug and 'store' in request.GET:
            store_slug = request.GET.get('store')
        
        # Try to get store by slug
        if store_slug:
            try:
                derived_store = Store.objects.get(slug=store_slug)
                context['store_theme'] = derived_store.get_theme_settings()
                return context
            except Store.DoesNotExist:
                pass
        
        # Default theme settings when no store is available
        context['store_theme'] = {
            'name': 'StoreLoop',
            'theme_name': 'light',
            'primary_color': '#3b82f6',
            'secondary_color': '#1f2937',
            'font_choice': 'sans',
            'logo_url': None,
            'custom_css': '',
            'custom_js': '',
            'theme_version': 'v1',
        }
    
    return context