from django import template
import locale

register = template.Library()

@register.filter
def currency(value):
    """Format currency based on locale"""
    try:
        locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
        return locale.currency(float(value), grouping=True)
    except:
        # Fallback to ₹ symbol if locale not available
        return f"₹{value}"