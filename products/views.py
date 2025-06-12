from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product
from stores.models import Store

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_template_names(self):
        # Check if there's a current store with a theme
        current_store = getattr(self.request, 'current_store', None)
        if current_store and current_store.theme_name:
            # Try to use the store's theme template first
            return [
                f'stores/themes/{current_store.theme_name}.html',
                'products/product_list.html'  # Fallback to default
            ]
        return ['products/product_list.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'All Products'
        context['stores'] = Store.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related products from the same store
        store = self.object.store
        context['related_products'] = Product.objects.filter(store=store).exclude(id=self.object.id)[:3]
        return context