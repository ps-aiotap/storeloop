from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from django.conf import settings
import pandas as pd
import json
import requests
from .models import Store, Product, Order, SellerProfile, ProductUploadBatch
from .forms import StoreOnboardingForm, ProductForm, ProductUploadForm
from .tasks import send_whatsapp_notification, generate_ai_description
from .utils import generate_gst_invoice_pdf

@login_required
def seller_onboarding(request):
    """4-step seller onboarding wizard"""
    step = request.GET.get('step', '1')
    store = getattr(request.user, 'owned_stores', Store.objects.none()).first()
    
    if step == '1':  # Logo & Basic Info
        if request.method == 'POST':
            # Create store with basic info
            store_name = request.POST.get('name', '')
            store_description = request.POST.get('description', '')
            
            if not store:
                store = Store.objects.create(
                    name=store_name,
                    description=store_description,
                    owner=request.user
                )
            else:
                store.name = store_name
                store.description = store_description
                store.save()
            
            return redirect('/stores/onboarding/?step=2')
        else:
            form = StoreOnboardingForm(instance=store)
        return render(request, 'stores/onboarding_step1.html', {'form': form, 'step': 1})
    
    elif step == '2':  # Theme Selection
        if request.method == 'POST':
            if store:
                store.theme = request.POST.get('theme', 'minimal')
                store.primary_color = request.POST.get('primary_color', '#3B82F6')
                store.secondary_color = request.POST.get('secondary_color', '#10B981')
                store.font_family = request.POST.get('font_family', 'sans-serif')
                store.save()
            return redirect('/stores/onboarding/?step=3')
        return render(request, 'stores/onboarding_step2.html', {'store': store, 'step': 2})
    
    elif step == '3':  # Sample Products
        if request.method == 'POST':
            # Create sample products
            sample_products = [
                {'name': 'Sample Product 1', 'price': 999, 'stock': 10},
                {'name': 'Sample Product 2', 'price': 1499, 'stock': 5},
            ]
            for product_data in sample_products:
                Product.objects.get_or_create(
                    store=store,
                    name=product_data['name'],
                    defaults=product_data
                )
            return redirect('/stores/onboarding/?step=4')
        return render(request, 'stores/onboarding_step3.html', {'store': store, 'step': 3})
    
    elif step == '4':  # Sample Products
        if request.method == 'POST':
            # Create sample products
            sample_products = [
                {'name': 'Sample Product 1', 'price': 999, 'stock': 10},
                {'name': 'Sample Product 2', 'price': 1499, 'stock': 5},
            ]
            for product_data in sample_products:
                Product.objects.get_or_create(
                    store=store,
                    name=product_data['name'],
                    defaults=product_data
                )
            return redirect('/stores/onboarding/?step=5')
        return render(request, 'stores/onboarding_step4.html', {'store': store, 'step': 4})
    
    elif step == '5':  # Razorpay Configuration
        if request.method == 'POST':
            store.razorpay_key_id = request.POST.get('razorpay_key_id', '')
            store.razorpay_key_secret = request.POST.get('razorpay_key_secret', '')
            store.gst_number = request.POST.get('gst_number', '')
            store.business_address = request.POST.get('business_address', '')
            store.onboarding_completed = True
            store.is_published = True
            store.save()
            messages.success(request, _('Store setup completed successfully!'))
            return redirect('seller_dashboard')
        return render(request, 'stores/onboarding_step5.html', {'store': store, 'step': 5})

@login_required
def seller_dashboard(request):
    """Mobile-first seller dashboard"""
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        # Redirect to onboarding if no store exists
        return redirect('seller_onboarding')
    
    # Basic analytics
    total_orders = Order.objects.filter(store=store).count()
    total_sales = sum(order.total_amount for order in Order.objects.filter(store=store, status='delivered'))
    pending_orders = Order.objects.filter(store=store, status='pending').count()
    products_count = Product.objects.filter(store=store, is_active=True).count()
    
    # Recent orders
    recent_orders = Order.objects.filter(store=store).order_by('-created_at')[:5]
    
    # Low stock products
    low_stock_products = Product.objects.filter(store=store, stock__lte=5, is_active=True)
    
    context = {
        'store': store,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'pending_orders': pending_orders,
        'products_count': products_count,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'stores/dashboard.html', context)

@login_required
def partner_admin_dashboard(request):
    """NGO partner admin dashboard"""
    profile = get_object_or_404(SellerProfile, user=request.user, is_partner_admin=True)
    
    # Switch store view
    selected_store_id = request.GET.get('store_id')
    if selected_store_id:
        selected_store = get_object_or_404(Store, id=selected_store_id, partner_admins=profile)
    else:
        selected_store = profile.managed_stores.first()
    
    # Aggregate metrics for all managed stores
    managed_stores = profile.managed_stores.all()
    total_stores = managed_stores.count()
    total_artisans = sum(store.owner_set.count() for store in managed_stores)
    total_revenue = sum(
        sum(order.total_amount for order in store.orders.filter(status='delivered'))
        for store in managed_stores
    )
    
    context = {
        'profile': profile,
        'managed_stores': managed_stores,
        'selected_store': selected_store,
        'total_stores': total_stores,
        'total_artisans': total_artisans,
        'total_revenue': total_revenue,
    }
    return render(request, 'stores/partner_dashboard.html', context)

@login_required
def product_upload(request):
    """Excel/CSV product upload"""
    store = get_object_or_404(Store, owner=request.user)
    
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_batch = ProductUploadBatch.objects.create(
                store=store,
                file=form.cleaned_data['file']
            )
            
            try:
                # Process Excel/CSV file
                file_path = upload_batch.file.path
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)
                
                upload_batch.total_rows = len(df)
                errors = []
                successful = 0
                
                for index, row in df.iterrows():
                    try:
                        Product.objects.create(
                            store=store,
                            name=row.get('name', ''),
                            description=row.get('description', ''),
                            price=float(row.get('price', 0)),
                            stock=int(row.get('stock', 0)),
                            category=row.get('category', ''),
                            image_url=row.get('image_url', ''),
                            material=row.get('material', ''),
                            region=row.get('region', ''),
                            style=row.get('style', ''),
                        )
                        successful += 1
                    except Exception as e:
                        errors.append(f"Row {index + 1}: {str(e)}")
                
                upload_batch.successful_imports = successful
                upload_batch.failed_imports = len(errors)
                upload_batch.errors = errors
                upload_batch.status = 'completed'
                upload_batch.save()
                
                messages.success(request, f'Uploaded {successful} products successfully!')
                if errors:
                    messages.warning(request, f'{len(errors)} products failed to upload.')
                
            except Exception as e:
                upload_batch.status = 'failed'
                upload_batch.errors = [str(e)]
                upload_batch.save()
                messages.error(request, f'Upload failed: {str(e)}')
            
            return redirect('product_upload')
    else:
        form = ProductUploadForm()
    
    recent_uploads = ProductUploadBatch.objects.filter(store=store).order_by('-created_at')[:5]
    return render(request, 'stores/product_upload.html', {'form': form, 'recent_uploads': recent_uploads})

@login_required
def product_add(request):
    """Add single product with AI description support"""
    store = get_object_or_404(Store, owner=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, _('Product added successfully!'))
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'stores/product_add.html', {'form': form, 'store': store})

@login_required
def product_edit(request, product_id):
    """Edit existing product"""
    store = get_object_or_404(Store, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, _('Product updated successfully!'))
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'stores/product_edit.html', {'form': form, 'product': product, 'store': store})

@csrf_exempt
def generate_product_description(request):
    """AI product description generator"""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        product_name = data.get('product_name', '')
        material = data.get('material', '')
        region = data.get('region', '')
        style = data.get('style', '')
        language = data.get('language', 'en')
        
        # Generate AI description (async task)
        task = generate_ai_description.delay(product_name, material, region, style, language)
        
        return JsonResponse({
            'task_id': task.id,
            'status': 'processing'
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def check_ai_task(request, task_id):
    """Check AI description generation status"""
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    if task.ready():
        if task.successful():
            return JsonResponse({
                'status': 'completed',
                'result': task.result
            })
        else:
            return JsonResponse({
                'status': 'failed',
                'error': str(task.info)
            })
    else:
        return JsonResponse({'status': 'processing'})

@login_required
def order_detail(request, order_id):
    """Order detail with status update"""
    order = get_object_or_404(Order, order_id=order_id, store__owner=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            old_status = order.status
            order.status = new_status
            order.save()
            
            # Send WhatsApp notification on status change
            if old_status != new_status:
                send_whatsapp_notification.delay(order.id, 'status_update')
            
            messages.success(request, f'Order status updated to {new_status}')
            return redirect('order_detail', order_id=order_id)
    
    return render(request, 'stores/order_detail.html', {'order': order})

@login_required
def download_gst_invoice(request, order_id):
    """Generate and download GST invoice PDF"""
    order = get_object_or_404(Order, order_id=order_id, store__owner=request.user)
    
    pdf_content = generate_gst_invoice_pdf(order)
    
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_id}.pdf"'
    return response

@login_required
def analytics_api(request):
    """API endpoint for seller analytics"""
    store = get_object_or_404(Store, owner=request.user)
    
    # Sales data for charts
    orders = Order.objects.filter(store=store, status='delivered')
    
    # Monthly sales
    monthly_sales = {}
    for order in orders:
        month = order.created_at.strftime('%Y-%m')
        monthly_sales[month] = monthly_sales.get(month, 0) + float(order.total_amount)
    
    # Top products
    product_sales = {}
    for order in orders:
        product_name = order.product.name
        product_sales[product_name] = product_sales.get(product_name, 0) + order.quantity
    
    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return JsonResponse({
        'monthly_sales': monthly_sales,
        'top_products': dict(top_products),
        'total_orders': orders.count(),
        'total_revenue': sum(float(order.total_amount) for order in orders)
    })

def set_language(request):
    """Set user language preference"""
    if request.method == 'POST':
        language = request.POST.get('language', 'en')
        if hasattr(request.user, 'sellerprofile'):
            request.user.sellerprofile.language_preference = language
            request.user.sellerprofile.save()
        
        from django.utils import translation
        translation.activate(language)
        request.session['django_language'] = language
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

def store_listing(request):
    """List all published stores"""
    # Show only published stores to regular visitors
    # Admins can see all stores
    if request.user.is_authenticated and request.user.is_superuser:
        stores = Store.objects.exclude(slug='').order_by('-created_at')
    else:
        stores = Store.objects.filter(is_published=True).exclude(slug='').order_by('-created_at')
    return render(request, 'stores/store_listing.html', {'stores': stores})

def store_homepage(request, store_slug):
    """Store homepage with homepage blocks"""
    from django.http import HttpResponse
    
    # Try to find store by slug
    try:
        store = Store.objects.get(slug=store_slug)
    except Store.DoesNotExist:
        return HttpResponse("<h1>Store not found</h1><p><a href='/stores/'>Browse all stores</a></p>")
    
    # Check if store is published (unless user is admin/owner)
    if not store.is_published:
        if not request.user.is_authenticated or (request.user != store.owner and not request.user.is_superuser):
            return HttpResponse("<h1>Store not available</h1><p>This store is not published yet.</p><p><a href='/stores/'>Browse all stores</a></p>")
    
    # Get homepage blocks
    homepage_blocks = store.homepage_blocks.filter(is_active=True).order_by('order')
    
    # Get featured products
    featured_products = store.store_products.filter(is_active=True)[:6]
    
    # Simple HTML response for now
    blocks_html = "<br>".join([f"<div><h3>{block.title}</h3><p>{block.content}</p></div>" for block in homepage_blocks])
    # Format currency based on locale
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
        products_html = "<br>".join([f"<div>{product.name} - {locale.currency(float(product.price), grouping=True)}</div>" for product in featured_products])
    except:
        # Fallback to ₹ symbol if locale not available
        products_html = "<br>".join([f"<div>{product.name} - ₹{product.price}</div>" for product in featured_products])
    
    return HttpResponse(f"""
    <h1>{store.name}</h1>
    <p>{store.description}</p>
    <h2>Homepage Blocks:</h2>
    {blocks_html}
    <h2>Featured Products:</h2>
    {products_html}
    """)