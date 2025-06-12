from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import Store
from .forms import StoreThemeForm
from products.models import Product

@login_required
def store_theme_settings(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    
    if request.method == 'POST':
        form = StoreThemeForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Theme settings updated successfully!')
            return redirect('store_theme_settings', store_id=store.id)
    else:
        form = StoreThemeForm(instance=store)
    
    return render(request, 'stores/theme_settings.html', {
        'form': form,
        'store': store
    })

class StoreProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        self.store = get_object_or_404(Store, slug=self.kwargs['slug'])
        return Product.objects.filter(store=self.store)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = self.store
        context['page_title'] = f"Products from {self.store.name}"
        return context