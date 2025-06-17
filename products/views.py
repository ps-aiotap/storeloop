from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.http import Http404
from .models import Product
from stores.models import Store

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_template_names(self):
        # If no store is selected, show the store list template
        if not hasattr(self.request, 'current_store') or not self.request.current_store:
            return ['products/store_list.html']
        
        # Otherwise use the unified theme template
        return ['stores/theme_view.html']
    
    def get_queryset(self):
        # Filter products by current store
        if hasattr(self.request, 'current_store') and self.request.current_store:
            return Product.objects.filter(store=self.request.current_store)
        
        # If no store context, return empty queryset
        return Product.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # If no current store, provide a list of available stores
        if not hasattr(self.request, 'current_store') or not self.request.current_store:
            context['page_title'] = 'Browse Stores'
            context['stores'] = Store.objects.all()
            context['no_store_selected'] = True
        else:
            context['page_title'] = f'Products from {self.request.current_store.name}'
            context['stores'] = Store.objects.all()
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_template_names(self):
        # Use the product detail template
        return ['stores/product_detail.html', 'products/product_detail.html']
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Set the current store based on the product's store
        self.request.current_store = obj.store
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related products from the same store
        store = self.object.store
        context['related_products'] = Product.objects.filter(store=store).exclude(id=self.object.id)[:3]
        return context