def send_whatsapp_notification(order_id, notification_type='order_confirmation'):
    """WhatsApp notifications using mock service for demo"""
    try:
        from .mock_services import MockWhatsAppService
        from .models import Order
        
        order = Order.objects.get(id=order_id)
        
        if notification_type == 'order_confirmation':
            message = f"Order confirmed! Order ID: {order.order_id}. Total: ₹{order.total_amount}."
        elif notification_type == 'status_update':
            message = f"Order {order.order_id} status: {order.get_status_display()}"
        else:
            message = f"Update for order {order.order_id}"
        
        result = MockWhatsAppService.send_notification(
            phone=order.customer_phone,
            message=message,
            template_type=notification_type
        )
        
        print(f"WhatsApp Mock: {result}")
        return result
    except Exception as e:
        print(f"WhatsApp failed: {str(e)}")
        return {'success': False, 'error': str(e)}

def generate_ai_description(product_name, material, region, style, language='en'):
    """AI description generation using mock service for demo"""
    try:
        from .mock_services import MockAIService
        
        result = MockAIService.generate_description(
            product_name=product_name,
            material=material,
            region=region,
            style=style,
            language=language
        )
        
        print(f"AI Mock: {result}")
        return result
    except Exception as e:
        print(f"AI generation failed: {str(e)}")
        return {'success': False, 'error': str(e)}