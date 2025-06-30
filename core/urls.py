from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render, redirect
from .sitemaps import sitemaps
from .robots import robots_txt, security_txt

def homepage(request):
    return render(request, 'home.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = request.POST.get('email', '')
            user.save()
            
            # Save customer info
            from stores.models import Customer
            phone = request.POST.get('phone', '')
            if phone:
                Customer.objects.update_or_create(
                    phone=phone,
                    defaults={
                        'name': user.username,
                        'email': user.email,
                        'street': request.POST.get('street', ''),
                        'city': request.POST.get('city', ''),
                        'state': request.POST.get('state', ''),
                        'pincode': request.POST.get('pincode', '')
                    }
                )
            
            login(request, user)
            return redirect('/stores/')  # Redirect customers to store listing, not onboarding
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('stores/', include('stores.urls')),
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('.well-known/security.txt', security_txt, name='security_txt'),
    
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('accounts/register/', register_view, name='register'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = custom_404