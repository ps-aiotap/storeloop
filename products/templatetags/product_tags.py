from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def is_new(product):
    """Return True if product was created within the last 7 days"""
    return product.created_at >= (timezone.now() - timedelta(days=7))

@register.filter
def is_limited(product):
    """Return True if product stock is 5 or less"""
    return product.stock <= 5

@register.filter
def is_bestseller(product):
    """Return True if product is in top 3 most ordered this month"""
    return product.is_bestseller()