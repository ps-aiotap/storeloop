def store_theme(request):
    """
    Context processor to inject store theme settings into all templates.
    """
    # Default theme settings
    theme_context = {
        'theme_name': 'minimal',
        'primary_color': 'blue',
        'font_choice': 'sans',
        'logo_url': None,
    }
    
    # Try to get the current store from the request
    current_store = getattr(request, 'current_store', None)
    
    if current_store:
        theme_context = {
            'theme_name': current_store.theme_name,
            'primary_color': current_store.primary_color,
            'font_choice': current_store.font_choice,
            'logo_url': current_store.logo.url if current_store.logo else None,
        }
    
    return {'store_theme': theme_context}