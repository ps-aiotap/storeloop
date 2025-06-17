from django import template
from django.utils.safestring import mark_safe
from ..models import TagType, Tag, ContactForm, TrustBadge

register = template.Library()

@register.filter
def filter_by_id(queryset, id_value):
    """Filter a queryset by ID"""
    try:
        return queryset.get(id=id_value)
    except:
        return None

@register.filter
def filter_by_slug(queryset, slug):
    """Filter a queryset by slug"""
    try:
        return queryset.get(slug=slug)
    except:
        return None

@register.filter
def get_tags(tag_type):
    """Get all tags for a tag type"""
    if tag_type:
        return tag_type.tags.all()
    return []

@register.simple_tag
def get_trust_badges(store):
    """Get all trust badges for a store"""
    return TrustBadge.objects.filter(store=store)

@register.simple_tag
def get_contact_forms(store):
    """Get all contact forms for a store"""
    return ContactForm.objects.filter(store=store)

@register.simple_tag
def get_tag_types():
    """Get all tag types"""
    return TagType.objects.all()

@register.simple_tag
def get_tags_by_type(tag_type_slug):
    """Get all tags for a tag type by slug"""
    try:
        tag_type = TagType.objects.get(slug=tag_type_slug)
        return tag_type.tags.all()
    except TagType.DoesNotExist:
        return []

@register.simple_tag
def get_product_count_by_tag(tag):
    """Get the number of products with a specific tag"""
    return tag.products.count()

@register.filter
def format_price(value):
    """Format a price with currency symbol"""
    try:
        return f"₹{float(value):.2f}"
    except (ValueError, TypeError):
        return value