from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Store, StoreHomepageBlock, HomepageBlock
from .forms import StoreThemeForm
from products.models import Product, ContactForm, TrustBadge
import json

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
        self.store = get_object_or_404(Store, slug=self.kwargs['store_slug'])
        return Product.objects.filter(store=self.store)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = self.store
        context['page_title'] = f"Products from {self.store.name}"
        return context

def store_homepage(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    homepage_blocks = StoreHomepageBlock.objects.filter(store=store, is_active=True).order_by('order')
    
    # Get contact forms and trust badges for this store
    contact_forms = ContactForm.objects.filter(store=store)
    trust_badges = TrustBadge.objects.filter(store=store)
    
    return render(request, 'stores/homepage.html', {
        'store': store,
        'homepage_blocks': homepage_blocks,
        'contact_forms': contact_forms,
        'trust_badges': trust_badges,
    })

@login_required
def store_homepage_editor(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    available_blocks = HomepageBlock.objects.all()
    current_blocks = StoreHomepageBlock.objects.filter(store=store).order_by('order')
    
    # Create JSON representation of current blocks for React
    current_blocks_json = []
    for block in current_blocks:
        current_blocks_json.append({
            'id': block.id,
            'block_type': block.block_type,
            'title': block.title,
            'content': block.content,
            'order': block.order,
            'is_active': block.is_active,
            'configuration': block.configuration
        })
    
    return render(request, 'stores/homepage_editor_react.html', {
        'store': store,
        'available_blocks': available_blocks,
        'current_blocks': current_blocks,
        'current_blocks_json': json.dumps(current_blocks_json)
    })

@login_required
def store_homepage_block_create(request, store_slug):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    try:
        data = json.loads(request.body)
        block_type = data.get('block_type')
        title = data.get('title', '')
        
        # Get the highest order value and add 1
        highest_order = StoreHomepageBlock.objects.filter(store=store).order_by('-order').first()
        order = (highest_order.order + 1) if highest_order else 0
        
        block = StoreHomepageBlock.objects.create(
            store=store,
            block_type=block_type,
            title=title,
            order=order,
            configuration={}
        )
        
        return JsonResponse({
            'status': 'success',
            'block_id': block.id,
            'block_type': block.block_type,
            'title': block.title,
            'order': block.order,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def store_homepage_block_update(request, store_slug, block_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    block = get_object_or_404(StoreHomepageBlock, id=block_id, store=store)
    
    try:
        data = json.loads(request.body)
        
        if 'title' in data:
            block.title = data['title']
        
        if 'content' in data:
            block.content = data['content']
        
        if 'configuration' in data:
            block.configuration = data['configuration']
        
        if 'order' in data:
            block.order = data['order']
        
        if 'is_active' in data:
            block.is_active = data['is_active']
        
        block.save()
        
        return JsonResponse({
            'status': 'success',
            'block_id': block.id,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def store_homepage_block_delete(request, store_slug, block_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    block = get_object_or_404(StoreHomepageBlock, id=block_id, store=store)
    
    try:
        block.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def store_homepage_blocks_reorder(request, store_slug):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    store = get_object_or_404(Store, slug=store_slug, owner=request.user)
    
    try:
        data = json.loads(request.body)
        block_order = data.get('block_order', [])
        
        for i, block_id in enumerate(block_order):
            block = StoreHomepageBlock.objects.get(id=block_id, store=store)
            block.order = i
            block.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)