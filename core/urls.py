from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def direct_test(request):
    return HttpResponse("<h1>Direct Test Works!</h1><p>URLs are working</p>")

urlpatterns = [
    path('direct-test/', direct_test),
    path('', include('stores.urls_userless')),
]

# Serve static files in development
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)