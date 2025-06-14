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
        # Always use the unified theme template
        return ['stores/theme_view.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'All Products'
        context['stores'] = Store.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_template_names(self):
        # Use the product detail template
        return ['stores/product_detail.html', 'products/product_detail.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related products from the same store
        store = self.object.store
        context['related_products'] = Product.objects.filter(store=store).exclude(id=self.object.id)[:3]
        return context