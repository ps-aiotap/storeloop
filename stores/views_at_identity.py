"""
Example StoreLoop views using AT Identity permissions
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from at_identity.auth.decorators import at_permission_required
from .models import Store, Product

@login_required
@at_permission_required('store.create')
def create_store(request):
    """Create store - requires AT Identity permission"""
    if request.method == 'POST':
        # Store creation logic
        store = Store.objects.create(
            name=request.POST['name'],
            owner=request.user
        )
        return redirect('store_detail', store.id)
    
    return render(request, 'stores/create_store.html')

@login_required
@at_permission_required('product.create')
def create_product(request, store_id):
    """Create product - requires AT Identity permission"""
    store = Store.objects.get(id=store_id, owner=request.user)
    
    if request.method == 'POST':
        # Product creation logic
        product = Product.objects.create(
            store=store,
            name=request.POST['name'],
            price=request.POST['price']
        )
        return redirect('product_detail', product.id)
    
    return render(request, 'stores/create_product.html', {'store': store})

@login_required
def dashboard(request):
    """Dashboard with AT Identity permissions"""
    from at_identity.auth.decorators import has_at_permission
    
    context = {
        'can_create_store': has_at_permission(request.user, 'store.create'),
        'can_manage_products': has_at_permission(request.user, 'product.create'),
        'can_view_analytics': has_at_permission(request.user, 'analytics.view'),
        'stores': Store.objects.filter(owner=request.user)
    }
    
    return render(request, 'stores/dashboard.html', context)