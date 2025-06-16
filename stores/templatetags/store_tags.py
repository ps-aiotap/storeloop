from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def sort_by(products, sort_type):
    """Sort products by the specified criteria"""
    if sort_type == 'price_low':
        return products.order_by('price')
    elif sort_type == 'price_high':
        return products.order_by('-price')
    elif sort_type == 'popular':
        return products.order_by('-views')
    else:  # newest
        return products.order_by('-created_at')

@register.filter
def filter_by_category(products, category_slug):
    """Filter products by category slug"""
    return products.filter(category__slug=category_slug)

@register.filter
def json_script(value, element_id):
    """Output the JSON representation of a value in a script tag."""
    json_str = json.dumps(value)
    return mark_safe(f'<script id="{element_id}" type="application/json">{json_str}</script>')