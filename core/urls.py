from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Custom error handlers
def custom_404_view(request, exception):
    from django.shortcuts import render
    return render(request, '404.html', status=404)

handler404 = custom_404_view

def home_redirect(request):
    return redirect('/stores/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('stores.urls')),
    path('stores/', include('stores.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('', home_redirect, name='home'),
]

# Serve static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)