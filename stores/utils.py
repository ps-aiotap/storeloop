from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import os

def generate_gst_invoice_pdf(order):
    """Generate GST-compliant invoice PDF"""
    
    # Calculate GST (18% for most products)
    gst_rate = 0.18
    base_amount = float(order.total_amount) / (1 + gst_rate)
    gst_amount = float(order.total_amount) - base_amount
    
    context = {
        'order': order,
        'store': order.store,
        'base_amount': round(base_amount, 2),
        'gst_amount': round(gst_amount, 2),
        'gst_rate': int(gst_rate * 100),
        'invoice_number': f"INV-{order.order_id}",
    }
    
    # Render HTML template
    html_string = render_to_string('stores/invoice_template.html', context)
    
    # Generate PDF
    html = HTML(string=html_string)
    css = CSS(string="""
        @page {
            size: A4;
            margin: 1cm;
        }
        body {
            font-family: Arial, sans-serif;
            font-size: 12px;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .invoice-details {
            margin-bottom: 20px;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        .table th, .table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .table th {
            background-color: #f2f2f2;
        }
        .total-row {
            font-weight: bold;
        }
    """)
    
    pdf = html.write_pdf(stylesheets=[css])
    return pdf

def get_store_from_domain(request):
    """Get store based on subdomain or custom domain"""
    host = request.get_host().lower()
    
    # Check for custom domain
    from .models import Store
    
    # Remove port if present
    if ':' in host:
        host = host.split(':')[0]
    
    # Check for subdomain (e.g., artisan.storeloop.in)
    if host.endswith('.storeloop.in'):
        subdomain = host.replace('.storeloop.in', '')
        try:
            return Store.objects.get(subdomain=subdomain, is_published=True)
        except Store.DoesNotExist:
            pass
    
    # Check for custom domain
    try:
        return Store.objects.get(custom_domain=host, is_published=True)
    except Store.DoesNotExist:
        pass
    
    return None

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip