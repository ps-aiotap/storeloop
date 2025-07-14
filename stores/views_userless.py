"""
Userless views for StoreLoop - Simplified without AT Identity dependencies
"""
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Store, Product
import requests
from django.conf import settings

def login_view(request):
    """Simple login form"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Mock authentication for testing
        if username == 'test' and password == 'test':
            request.session['at_identity_user_id'] = 1
            request.session['username'] = username
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials (use test/test)'})
    
    return render(request, 'login.html')

def logout_view(request):
    """Logout user"""
    request.session.flush()
    return redirect('login')

def create_store(request):
    """Create store - simplified without permission check"""
    user_id = request.session.get('at_identity_user_id')
    if not user_id:
        return redirect('login')
        
    if request.method == 'POST':
        store = Store.objects.create(
            name=request.POST['name'],
            owner_id=user_id,
            owner_username=request.session.get('username', 'test')
        )
        return redirect('dashboard')
    
    return render(request, 'stores/create_store.html')

def dashboard(request):
    """Dashboard for authenticated users"""
    user_id = request.session.get('at_identity_user_id')
    if not user_id:
        return redirect('login')
    
    stores = Store.objects.filter(owner_id=user_id)
    context = {
        'user': {
            'id': user_id,
            'username': request.session.get('username', 'test'),
            'is_authenticated': True
        },
        'stores': stores
    }
    return render(request, 'stores/dashboard.html', context)