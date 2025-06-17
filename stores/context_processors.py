from .models import Store

def store_theme(request):
    """
    Context processor to add store theme to template context
    """
    context = {}
    
    # Get current store from request (set by StoreMiddleware)
    current_store = getattr(request, 'current_store', None)
    
    if current_store:
        # Create store_theme context variable with safe defaults for new fields
        context['store_theme'] = {
            'name': current_store.name,
            'theme_name': current_store.theme_name,
            'primary_color': current_store.primary_color,
            'font_choice': current_store.font_choice,
            'logo_url': current_store.logo_url.url if current_store.logo_url else None,
            'custom_css': getattr(current_store, 'custom_css', ''),
            'custom_js': getattr(current_store, 'custom_js', ''),
            'theme_version': getattr(current_store, 'theme_version', 'v1'),
        }
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
                context['store_theme'] = {
                    'name': derived_store.name,
                    'theme_name': derived_store.theme_name,
                    'primary_color': derived_store.primary_color,
                    'font_choice': derived_store.font_choice,
                    'logo_url': derived_store.logo_url.url if derived_store.logo_url else None,
                    'custom_css': getattr(derived_store, 'custom_css', ''),
                    'custom_js': getattr(derived_store, 'custom_js', ''),
                    'theme_version': getattr(derived_store, 'theme_version', 'v1'),
                }
                return context
            except Store.DoesNotExist:
                pass
        
        # Default theme settings when no store is available
        context['store_theme'] = {
            'name': 'StoreLoop',
            'theme_name': 'light',
            'primary_color': '#3b82f6',
            'font_choice': 'sans',
            'logo_url': None,
            'custom_css': '',
            'custom_js': '',
            'theme_version': 'v1',
        }
    
    return context