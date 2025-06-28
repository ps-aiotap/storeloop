def store_theme(request):
    """Context processor to add store theme variables to templates"""
    context = {}
    
    if hasattr(request, 'store') and request.store:
        context.update({
            'store': request.store,
            'store_theme': {
                'primary_color': request.store.primary_color,
                'secondary_color': request.store.secondary_color,
                'font_family': request.store.font_family,
                'theme': request.store.theme,
            }
        })
    
    return context