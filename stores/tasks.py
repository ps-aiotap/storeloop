def send_whatsapp_notification(order_id, notification_type='order_confirmation'):
    """Stub for WhatsApp notifications"""
    print(f"WhatsApp notification stub: Order {order_id}, Type: {notification_type}")
    return f"Notification sent for order {order_id}"

def generate_ai_description(product_name, material, region, style, language='en'):
    """Stub for AI description generation"""
    if language == 'hi':
        short_desc = f"{product_name} - {material} से बना, {region} की पारंपरिक {style} शैली में।"
        long_desc = f"यह सुंदर {product_name} {region} के कुशल कारीगरों द्वारा {material} का उपयोग करके बनाया गया है।"
    else:
        short_desc = f"Beautiful {product_name} crafted from {material} in traditional {style} style from {region}."
        long_desc = f"This exquisite {product_name} is handcrafted by skilled artisans from {region} using premium {material}."
    
    return {
        'short_description': short_desc,
        'long_description': long_desc,
        'language': language
    }