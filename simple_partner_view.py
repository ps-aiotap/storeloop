#!/usr/bin/env python
"""Simple partner dashboard view for testing"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from stores.models import Store

@login_required
def simple_partner_dashboard(request):
    """Simple partner dashboard without complex logic"""
    
    # Get all stores
    managed_stores = Store.objects.all()[:10]
    
    # Add basic analytics
    for store in managed_stores:
        store.product_count = store.store_products.count()
        store.order_count = store.orders.count()
        store.total_revenue = round(sum(float(order.total_amount) for order in store.orders.all()), 2)
    
    # Create artisan list
    artisan_list = []
    for store in managed_stores:
        artisan_list.append({
            'id': store.owner.id if store.owner else 0,
            'name': store.owner.username if store.owner else 'Unknown',
            'store_name': store.name,
            'store_id': store.id,
            'product_count': store.product_count,
            'order_count': store.order_count,
            'revenue': round(store.total_revenue, 2),
        })
    
    context = {
        'managed_stores': managed_stores,
        'total_stores': len(managed_stores),
        'total_artisans': len(managed_stores),
        'total_orders': sum(store.order_count for store in managed_stores),
        'total_revenue': round(sum(store.total_revenue for store in managed_stores), 2),
        'artisan_list': artisan_list,
        'is_partner_admin': True,
    }
    
    return render(request, 'stores/partner_dashboard.html', context)

# Test the view directly
if __name__ == "__main__":
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    
    try:
        # Create test request
        factory = RequestFactory()
        request = factory.get('/test/')
        
        # Get test user
        user = User.objects.first()
        if not user:
            user = User.objects.create_user('testuser', 'test@test.com', 'password')
        request.user = user
        
        print("Testing simple partner dashboard...")
        response = simple_partner_dashboard(request)
        print(f"Success! Response status: {response.status_code}")
        print(f"Response type: {type(response)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()