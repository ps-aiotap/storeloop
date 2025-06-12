from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Store
from .forms import StoreThemeForm

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