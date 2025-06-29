from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from io import BytesIO
from django.conf import settings
import os

def generate_gst_invoice_pdf(order):
    """Generate GST-compliant invoice PDF using ReportLab"""
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Invoice header
    p.drawString(100, 750, f"INVOICE - {order.order_id}")
    p.drawString(100, 730, f"Store: {order.store.name}")
    p.drawString(100, 710, f"Customer: {order.customer_name}")
    p.drawString(100, 690, f"Product: {order.product.name}")
    p.drawString(100, 670, f"Quantity: {order.quantity}")
    p.drawString(100, 650, f"Amount: ₹{order.total_amount}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer.getvalue()

def get_store_from_domain(request):
    """Get store based on subdomain or custom domain"""
    host = request.get_host().lower()
    
    from .models import Store
    
    if ':' in host:
        host = host.split(':')[0]
    
    if host.endswith('.storeloop.in'):
        subdomain = host.replace('.storeloop.in', '')
        try:
            return Store.objects.get(subdomain=subdomain, is_published=True)
        except Store.DoesNotExist:
            pass
    
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