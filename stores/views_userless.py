"""
Userless views for StoreLoop
"""
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Store, Product
from at_identity.auth.decorators import at_permission_required

def login_view(request):
    """Simple login form"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate with AT Identity
        from at_identity.auth.backends_userless import UserlessATIdentityBackend
        backend = UserlessATIdentityBackend()
        user = backend.authenticate(request, username=username, password=password)
        
        if user:
            # Store user ID in session
            request.session['at_identity_user_id'] = user.id
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

def logout_view(request):
    """Logout user"""
    request.session.flush()
    return redirect('login')

@at_permission_required('store.create')
def create_store(request):
    """Create store with userless authentication"""
    if request.method == 'POST':
        store = Store.objects.create(
            name=request.POST['name'],
            owner_id=request.user.id,
            owner_username=request.user.username
        )
        return redirect('store_detail', store.id)
    
    return render(request, 'stores/create_store.html')

def dashboard(request):
    """Dashboard for authenticated users"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    stores = Store.objects.filter(owner_id=request.user.id)
    return render(request, 'stores/dashboard.html', {'stores': stores})