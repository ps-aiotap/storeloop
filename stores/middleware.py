from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from .utils import get_store_from_domain

class SubdomainMiddleware(MiddlewareMixin):
    """Handle subdomain and custom domain routing"""
    
    def process_request(self, request):
        # Skip for admin and API URLs
        if request.path.startswith('/admin/') or request.path.startswith('/api/'):
            return None
        
        store = get_store_from_domain(request)
        
        if store:
            # Set store in request for use in views
            request.store = store
            
            # If accessing store-specific URL, render store frontend
            if not request.path.startswith('/seller/'):
                return self.render_store_frontend(request, store)
        
        return None
    
    def render_store_frontend(self, request, store):
        """Render store frontend for customers"""
        from .models import Product
        
        if request.path == '/':
            # Store homepage
            products = Product.objects.filter(store=store, is_active=True)[:12]
            context = {
                'store': store,
                'products': products,
            }
            return render(request, 'stores/store_frontend.html', context)
        
        elif request.path.startswith('/product/'):
            # Product detail page
            product_slug = request.path.split('/')[-2]
            try:
                product = Product.objects.get(store=store, slug=product_slug, is_active=True)
                context = {
                    'store': store,
                    'product': product,
                }
                return render(request, 'stores/product_detail.html', context)
            except Product.DoesNotExist:
                return render(request, 'stores/404.html', {'store': store}, status=404)
        
        return None

class LanguageMiddleware(MiddlewareMixin):
    """Handle language preference for authenticated users"""
    
    def process_request(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'sellerprofile'):
            language = request.user.sellerprofile.language_preference
            if language:
                from django.utils import translation
                translation.activate(language)
                request.LANGUAGE_CODE = language
        
        return None