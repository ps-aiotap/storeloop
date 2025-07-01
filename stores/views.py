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
    """5-step seller onboarding wizard"""
    # Check if user came from customer registration - redirect them away
    from .models import Customer
    if Customer.objects.filter(name=request.user.username).exists():
        messages.info(request, 'You are registered as a customer. To create a store, please contact support.')
        return redirect('/stores/')
    
    step = request.GET.get('step', '1')
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        store = None
    
    if step == '1':  # Logo & Basic Info
        if request.method == 'POST':
            store_name = request.POST.get('name', '')
            store_description = request.POST.get('description', '')
            logo = request.FILES.get('logo')
            
            if not store:
                store = Store.objects.create(
                    name=store_name,
                    description=store_description,
                    owner=request.user,
                    logo=logo if logo else None
                )
            else:
                store.name = store_name
                store.description = store_description
                if logo:
                    store.logo = logo
                store.save()
            
            return redirect('/stores/onboarding/?step=2')
        return render(request, 'stores/onboarding_step1.html', {'store': store, 'step': 1})
    
    elif step == '2':  # Theme Selection
        if not store:
            return redirect('/stores/onboarding/?step=1')
        if request.method == 'POST':
            store.theme = request.POST.get('theme', 'minimal')
            store.primary_color = request.POST.get('primary_color', '#3B82F6')
            store.secondary_color = request.POST.get('secondary_color', '#10B981')
            store.font_family = request.POST.get('font_family', 'sans-serif')
            store.save()
            return redirect('/stores/onboarding/?step=3')
        return render(request, 'stores/onboarding_step2.html', {'store': store, 'step': 2})
    
    elif step == '3':  # Homepage Layout
        if not store:
            return redirect('/stores/onboarding/?step=1')
        if request.method == 'POST':
            from .models import StoreHomepageBlock
            
            hero_title = request.POST.get('hero_title', 'Welcome to Our Store')
            hero_content = request.POST.get('hero_content', 'Discover unique handcrafted items')
            StoreHomepageBlock.objects.get_or_create(
                store=store,
                block_type='hero_banner',
                defaults={
                    'title': hero_title,
                    'content': hero_content,
                    'order': 1
                }
            )
            
            about_title = request.POST.get('about_title', 'About Our Craft')
            about_content = request.POST.get('about_content', 'We create beautiful handmade items')
            StoreHomepageBlock.objects.get_or_create(
                store=store,
                block_type='text_block',
                defaults={
                    'title': about_title,
                    'content': about_content,
                    'order': 2
                }
            )
            
            return redirect('/stores/onboarding/?step=4')
        return render(request, 'stores/onboarding_step3.html', {'store': store, 'step': 3})
    
    elif step == '4':  # Sample Products
        if not store:
            return redirect('/stores/onboarding/?step=1')
        if request.method == 'POST':
            sample_products = [
                {'name': 'Sample Product 1', 'price': 999, 'stock': 10, 'description': 'Beautiful handcrafted item'},
                {'name': 'Sample Product 2', 'price': 1499, 'stock': 5, 'description': 'Premium artisan creation'},
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
        if not store:
            return redirect('/stores/onboarding/?step=1')
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
    
    return redirect('/stores/onboarding/?step=1')

@login_required
def seller_dashboard(request):
    """Mobile-first seller dashboard"""
    try:
        profile = SellerProfile.objects.get(user=request.user)
        if profile.is_partner_admin:
            return redirect('/stores/partner-dashboard/')
    except SellerProfile.DoesNotExist:
        pass
    
    try:
        store = Store.objects.get(owner=request.user)
        if not store.onboarding_completed:
            return redirect('seller_onboarding')
    except Store.DoesNotExist:
        return redirect('seller_onboarding')
    
    total_orders = Order.objects.filter(store=store).count()
    total_sales = sum(order.total_amount for order in Order.objects.filter(store=store, status='delivered'))
    pending_orders = Order.objects.filter(store=store, status='pending').count()
    products_count = Product.objects.filter(store=store, is_active=True).count()
    recent_orders = Order.objects.filter(store=store).order_by('-created_at')[:5]
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
    """NGO partner admin dashboard with multi-store switching and aggregate analytics"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get all stores for demo (in production, filter by partner relationship)
    managed_stores = Store.objects.filter(is_published=True)[:5]  # Limit for demo
    
    # Add analytics data to each store
    for store in managed_stores:
        store.product_count = store.store_products.count()
        store.order_count = store.orders.count()
        store.total_revenue = round(sum(float(order.total_amount) for order in store.orders.all()), 2)
    
    # Aggregate analytics
    total_stores = managed_stores.count()
    total_artisans = managed_stores.count()  # Assuming 1 artisan per store
    total_orders = sum(store.order_count for store in managed_stores)
    total_revenue = round(sum(store.total_revenue for store in managed_stores), 2)
    
    # Artisan list for management
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
        'total_stores': total_stores,
        'total_artisans': total_artisans,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'artisan_list': artisan_list,
    }
    
    return render(request, 'stores/partner_dashboard.html', context)

@login_required
def product_upload(request):
    """Excel/CSV product upload"""
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        messages.error(request, 'Please complete store setup first.')
        return redirect('seller_onboarding')
    
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_batch = ProductUploadBatch.objects.create(
                store=store,
                file=form.cleaned_data['file']
            )
            
            try:
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
                        name = str(row.get('name', '')).strip()
                        price = row.get('price', 0)
                        image_url = str(row.get('image_url', '')).strip()
                        
                        if not name:
                            errors.append(f"Row {index + 1}: Product name is required")
                            continue
                            
                        if not price or float(price) <= 0:
                            errors.append(f"Row {index + 1}: Valid price is required")
                            continue
                        
                        # Validate image URL if provided
                        if image_url:
                            from .mock_services import MockImageValidator
                            validation_result = MockImageValidator.validate_image_url(image_url)
                            if not validation_result['valid']:
                                errors.append(f"Row {index + 1}: Image URL invalid - {validation_result['error']}")
                                continue
                        
                        Product.objects.create(
                            store=store,
                            name=name,
                            description=str(row.get('description', '')).strip(),
                            price=float(price),
                            stock=int(row.get('stock', 0)),
                            category=str(row.get('category', '')).strip(),
                            image_url=str(row.get('image_url', '')).strip(),
                            material=str(row.get('material', '')).strip(),
                            region=str(row.get('region', '')).strip(),
                            style=str(row.get('style', '')).strip(),
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
    return render(request, 'stores/product_upload.html', {'form': form, 'recent_uploads': recent_uploads, 'store': store})

@login_required
def product_add(request):
    """Add single product with AI description support"""
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        messages.error(request, 'Please complete store setup first.')
        return redirect('seller_onboarding')
    
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

@csrf_exempt
def create_order(request):
    """Create order and Razorpay payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            customer_name = data.get('customer_name', 'Guest Customer')
            customer_email = data.get('customer_email', 'guest@example.com')
            customer_phone = data.get('customer_phone', '1234567890')
            customer_address = data.get('customer_address', 'Guest Address')
            
            product = Product.objects.get(id=product_id)
            store = product.store
            
            # Check stock availability
            if product.stock < quantity:
                return JsonResponse({'success': False, 'error': 'Insufficient stock'})
            
            # Calculate amounts
            from decimal import Decimal
            subtotal = product.price * quantity
            gst_amount = subtotal * Decimal('0.18')  # 18% GST
            total_amount = subtotal + gst_amount
            
            order = Order.objects.create(
                store=store,
                product=product,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                customer_address=customer_address,
                quantity=quantity,
                total_amount=total_amount,
                gst_amount=gst_amount
            )
            
            # Save address to UserAddress model if user is authenticated
            if hasattr(request, 'user') and request.user.is_authenticated:
                from .models import UserAddress
                addr_parts = customer_address.split(',')
                user_address = UserAddress.objects.create(
                    user=request.user,
                    street=addr_parts[0].strip() if len(addr_parts) > 0 else customer_address,
                    city=addr_parts[1].strip() if len(addr_parts) > 1 else '',
                    state=addr_parts[2].split('-')[0].strip() if len(addr_parts) > 2 else '',
                    pincode=addr_parts[2].split('-')[1].strip() if len(addr_parts) > 2 and '-' in addr_parts[2] else ''
                )
                order.delivery_address = user_address
                order.save()
            
            # Reduce stock
            product.stock -= quantity
            product.save()
            
            return JsonResponse({
                'success': True,
                'order_id': order.order_id,
                'total_amount': float(total_amount),
                'razorpay_order_id': f'order_{order.id}',
                'message': f'Order placed successfully! Total: ₹{total_amount:.2f}'
            })
            
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def get_customer_info(request):
    """Get customer info by phone or username for auto-fill"""
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        username = data.get('username')
        
        try:
            from .models import Customer
            if phone:
                customer = Customer.objects.get(phone=phone)
            elif username:
                customer = Customer.objects.get(name=username)
            else:
                return JsonResponse({'success': False, 'error': 'Phone or username required'})
                
            return JsonResponse({
                'success': True,
                'customer': {
                    'name': customer.name,
                    'email': customer.email,
                    'phone': customer.phone,
                    'street': customer.street,
                    'city': customer.city,
                    'state': customer.state,
                    'pincode': customer.pincode
                }
            })
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Customer not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def get_customer_addresses(request):
    """Get all customer addresses for selection"""
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        
        try:
            from django.contrib.auth.models import User
            from .models import UserAddress
            
            user = User.objects.get(username=username)
            addresses_qs = UserAddress.objects.filter(user=user).order_by('-created_at')
            
            addresses = []
            for addr in addresses_qs:
                addresses.append({
                    'id': addr.id,
                    'name': user.username,
                    'email': user.email,
                    'phone': '',  # Phone not stored in UserAddress
                    'street': addr.street,
                    'city': addr.city,
                    'state': addr.state,
                    'pincode': addr.pincode,
                    'landmark': addr.landmark,
                    'full_address': f"{addr.street}, {addr.city}, {addr.state} - {addr.pincode}"
                })
            
            return JsonResponse({
                'success': True,
                'addresses': addresses
            })
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def analytics_api(request):
    """API endpoint for seller analytics"""
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        return JsonResponse({'error': 'Store not found'}, status=404)
    
    orders = Order.objects.filter(store=store, status='delivered')
    
    monthly_sales = {}
    for order in orders:
        month = order.created_at.strftime('%Y-%m')
        monthly_sales[month] = monthly_sales.get(month, 0) + float(order.total_amount)
    
    product_sales = {}
    for order in orders:
        product_name = order.product.name
        product_sales[product_name] = product_sales.get(product_name, 0) + order.quantity
    
    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    
    debug_info = {
        'store_name': store.name,
        'store_published': store.is_published,
        'onboarding_completed': store.onboarding_completed,
        'total_products': store.store_products.count(),
        'active_products': store.store_products.filter(is_active=True).count()
    }
    
    return JsonResponse({
        'monthly_sales': monthly_sales,
        'top_products': dict(top_products),
        'total_orders': orders.count(),
        'total_revenue': sum(float(order.total_amount) for order in orders),
        'debug': debug_info if request.user.is_superuser else None
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

def hindi_test_page(request):
    """Hindi test page to verify Unicode support"""
    return render(request, 'stores/hindi_test.html')

def customer_register(request):
    """Customer registration with address fields"""
    if request.method == 'POST':
        from django.contrib.auth.models import User
        from .models import UserAddress
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        try:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create address
            UserAddress.objects.create(
                user=user,
                street=street,
                city=city,
                state=state,
                pincode=pincode,
                is_default=True
            )
            
            # Login user
            from django.contrib.auth import login
            login(request, user)
            
            messages.success(request, 'Registration successful!')
            return redirect('/stores/')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'accounts/register.html')

def store_listing(request):
    """List all published stores"""
    if request.user.is_authenticated and request.user.is_superuser:
        stores = Store.objects.exclude(slug='').exclude(name='').order_by('-created_at')
    else:
        stores = Store.objects.filter(
            is_published=True, 
            onboarding_completed=True
        ).exclude(slug='').exclude(name='').order_by('-created_at')
    
    return render(request, 'stores/store_listing.html', {'stores': stores})

def store_homepage(request, store_slug):
    """Store homepage with homepage blocks"""
    try:
        store = Store.objects.get(slug=store_slug)
    except Store.DoesNotExist:
        return HttpResponse("<h1>Store not found</h1><p><a href='/stores/'>Browse all stores</a></p>")
    
    if not store.is_published:
        if not request.user.is_authenticated or (request.user != store.owner and not request.user.is_superuser):
            return HttpResponse("<h1>Store not available</h1><p>This store is not published yet.</p><p><a href='/stores/'>Browse all stores</a></p>")
    
    homepage_blocks = store.homepage_blocks.filter(is_active=True).order_by('order')
    featured_products = store.store_products.filter(is_active=True)[:6]
    
    context = {
        'store': store,
        'homepage_blocks': homepage_blocks,
        'featured_products': featured_products,
    }
    return render(request, 'stores/store_homepage.html', context)

def hindi_test_page(request):
    """Hindi test page to verify Unicode support"""
    return render(request, 'stores/hindi_test.html')