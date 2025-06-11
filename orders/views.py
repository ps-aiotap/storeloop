import json
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from products.models import Product
from .models import Order, OrderItem

def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        # Create Razorpay order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        payment_data = {
            'amount': int(product.price * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': f'receipt_{product.id}',
            'payment_capture': 1  # Auto-capture
        }
        
        razorpay_order = client.order.create(data=payment_data)
        
        context = {
            'product': product,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'callback_url': request.build_absolute_uri(reverse('payment_callback')),
        }
        
        return render(request, 'orders/checkout.html', context)
    
    return redirect('product_detail', pk=product_id)

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        payment_data = json.loads(request.body)
        razorpay_order_id = payment_data.get('razorpay_order_id')
        razorpay_payment_id = payment_data.get('razorpay_payment_id')
        
        # Verify payment signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            # Get payment details
            payment = client.payment.fetch(razorpay_payment_id)
            product_id = int(payment['notes'].get('product_id'))
            product = get_object_or_404(Product, id=product_id)
            
            # Create order
            order = Order.objects.create(
                customer_name=payment_data.get('customer_name'),
                customer_email=payment_data.get('customer_email'),
                customer_phone=payment_data.get('customer_phone'),
                shipping_address=payment_data.get('shipping_address'),
                total_amount=product.price,
                payment_id=razorpay_payment_id,
                razorpay_order_id=razorpay_order_id,
                status='processing'
            )
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.price
            )
            
            # Send confirmation email
            send_order_confirmation_email(order)
            
            return JsonResponse({'status': 'success', 'order_id': order.id})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/confirmation.html', {'order': order})

def send_order_confirmation_email(order):
    subject = f'Order Confirmation - StoreLoop #{order.id}'
    message = render_to_string('orders/email/confirmation_email.html', {
        'order': order,
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.customer_email],
        html_message=message,
    )