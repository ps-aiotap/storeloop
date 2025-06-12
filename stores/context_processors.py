def store_theme(request):
    """
    Context processor to add store theme to template context
    """
    context = {}
    
    # Get current store from request (set by StoreThemeMiddleware)
    current_store = getattr(request, 'current_store', None)
    
    if current_store:
        # Create store_theme context variable
        context['store_theme'] = {
            'name': current_store.name,
            'theme_name': current_store.theme_name,
            'primary_color': current_store.primary_color,
            'font_choice': current_store.font_choice,
            'logo_url': current_store.logo.url if current_store.logo else None,
            'custom_css': current_store.custom_css,
            'custom_js': current_store.custom_js,
            'theme_version': current_store.theme_version,
        }
    
    return context