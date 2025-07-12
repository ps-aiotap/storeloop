from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import HttpResponse

# Custom error handlers
def custom_404_view(request, exception):
    from django.shortcuts import render
    return render(request, '404.html', status=404)

handler404 = custom_404_view

def home_redirect(request):
    return redirect('/stores/')

def debug_partner(request):
    """Direct partner dashboard bypass"""
    try:
        from stores.models import Store
        stores = Store.objects.all()[:5]
        html = "<h1>Debug Partner Dashboard</h1>"
        for store in stores:
            html += f"<p>Store {store.id}: {store.name}</p>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"<h1>Debug Error</h1><p>{str(e)}</p>")

urlpatterns = [
    # path('admin/', admin.site.urls),  # Removed for userless system
    path('debug-partner/', debug_partner, name='debug_partner'),
    path('', include('stores.urls_userless')),
    path('accounts/', include('stores.urls')),
    path('stores/', include('stores.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    # path('crm/', include('artisan_crm.urls')),  # Removed for userless system
    path('', home_redirect, name='home'),
]

# Serve static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)