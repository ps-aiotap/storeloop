import os
from typing import Dict, Any, Literal

CRM_MODE = os.environ.get('CRM_MODE', 'STORELOOP').upper()

def get_crm_mode() -> Literal["STORELOOP", "AIO"]:
    """Get current CRM mode from environment"""
    return "AIO" if CRM_MODE == "AIO" else "STORELOOP"

def get_mode_config() -> Dict[str, Any]:
    """Get mode-specific configuration"""
    mode = get_crm_mode()
    
    configs = {
        "STORELOOP": {
            "app_name": "StoreLoop CRM",
            "primary_color": "#10B981",
            "lead_stages": ["Inquiry", "Interested", "Order Placed", "Delivered", "Repeat Customer"],
            "default_tags": ["artisan", "handmade", "whatsapp_customer"],
            "channels": ["whatsapp", "phone", "email"],
            "intent_categories": ["product_inquiry", "order_status", "complaint", "compliment", "general"]
        },
        "AIO": {
            "app_name": "AioTap CRM",
            "primary_color": "#3B82F6",
            "lead_stages": ["Lead", "Qualified", "Proposal", "Negotiation", "Won", "Lost"],
            "default_tags": ["ai_consulting", "b2b", "founder_led"],
            "channels": ["email", "upwork", "phone", "whatsapp"],
            "intent_categories": ["project_inquiry", "consultation_request", "follow_up", "pricing", "general"]
        }
    }
    
    return configs[mode]

def get_template_context() -> Dict[str, Any]:
    """Get template context for current mode"""
    config = get_mode_config()
    
    return {
        "crm_mode": get_crm_mode().lower(),
        "app_name": config["app_name"],
        "primary_color": config["primary_color"],
        "is_storeloop": get_crm_mode() == "STORELOOP",
        "is_aiotap": get_crm_mode() == "AIO"
    }

def filter_by_mode(queryset, mode_field='mode'):
    """Filter queryset by current mode or shared items"""
    mode = get_crm_mode().lower()
    return queryset.filter(**{f"{mode_field}__in": [mode, 'shared']})

class ModeContextMixin:
    """Mixin to add mode context to views"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_template_context())
        return context