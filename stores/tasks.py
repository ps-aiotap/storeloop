from celery import shared_task
from django.conf import settings
import requests
import json
from .models import Order

@shared_task
def send_whatsapp_notification(order_id, notification_type='order_confirmation'):
    """Send WhatsApp notification for orders"""
    try:
        order = Order.objects.get(id=order_id)
        
        if notification_type == 'order_confirmation':
            # Send to buyer
            buyer_message = f"""
🛍️ Order Confirmation - {order.store.name}

Order ID: {order.order_id}
Product: {order.product.name}
Quantity: {order.quantity}
Total: ₹{order.total_amount}

Thank you for your purchase!
            """.strip()
            
            send_whatsapp_message(order.customer_phone, buyer_message)
            
            # Send to seller
            seller_message = f"""
🔔 New Order Received!

Order ID: {order.order_id}
Customer: {order.customer_name}
Product: {order.product.name}
Amount: ₹{order.total_amount}

Please process this order.
            """.strip()
            
            seller_phone = order.store.owner.sellerprofile.whatsapp_number
            if seller_phone:
                send_whatsapp_message(seller_phone, seller_message)
        
        elif notification_type == 'status_update':
            # Send status update to buyer
            status_message = f"""
📦 Order Update - {order.store.name}

Order ID: {order.order_id}
Status: {order.get_status_display()}

Track your order for updates.
            """.strip()
            
            send_whatsapp_message(order.customer_phone, status_message)
        
        # Mark as sent
        order.whatsapp_sent = True
        order.save()
        
        return f"WhatsApp notification sent for order {order.order_id}"
        
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        return f"Failed to send WhatsApp: {str(e)}"

def send_whatsapp_message(phone_number, message):
    """Send WhatsApp message via Twilio or Gupshup (stub implementation)"""
    # Stub implementation - replace with actual API calls
    
    # Option 1: Twilio WhatsApp API
    if hasattr(settings, 'TWILIO_WHATSAPP_ENABLED') and settings.TWILIO_WHATSAPP_ENABLED:
        try:
            # Twilio implementation
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=message,
                from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
                to=f'whatsapp:+91{phone_number}'
            )
            return message.sid
        except Exception as e:
            print(f"Twilio WhatsApp error: {e}")
    
    # Option 2: Gupshup API
    elif hasattr(settings, 'GUPSHUP_API_KEY') and settings.GUPSHUP_API_KEY:
        try:
            url = "https://api.gupshup.io/sm/api/v1/msg"
            headers = {
                'apikey': settings.GUPSHUP_API_KEY,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'channel': 'whatsapp',
                'source': settings.GUPSHUP_SOURCE_NUMBER,
                'destination': f'91{phone_number}',
                'message': json.dumps({
                    'type': 'text',
                    'text': message
                })
            }
            
            response = requests.post(url, headers=headers, data=data)
            return response.json()
        except Exception as e:
            print(f"Gupshup WhatsApp error: {e}")
    
    # Stub implementation for development
    else:
        print(f"WhatsApp Stub: Sending to {phone_number}")
        print(f"Message: {message}")
        return "stub_message_id"

@shared_task
def generate_ai_description(product_name, material, region, style, language='en'):
    """Generate AI product description using OpenRouter or Groq"""
    try:
        # Prepare prompt
        if language == 'hi':
            prompt = f"""
एक भारतीय कारीगर उत्पाद के लिए आकर्षक विवरण लिखें:

उत्पाद: {product_name}
सामग्री: {material}
क्षेत्र: {region}
शैली: {style}

कृपया एक छोटा (50 शब्द) और एक विस्तृत (150 शब्द) विवरण प्रदान करें।
            """.strip()
        else:
            prompt = f"""
Write an engaging product description for an Indian artisan product:

Product: {product_name}
Material: {material}
Region: {region}
Style: {style}

Please provide both a short description (50 words) and a detailed description (150 words).
            """.strip()
        
        # Option 1: OpenRouter API
        if hasattr(settings, 'OPENROUTER_API_KEY') and settings.OPENROUTER_API_KEY:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Parse short and long descriptions
                lines = content.split('\n')
                short_desc = ""
                long_desc = ""
                
                for line in lines:
                    if 'short' in line.lower() or '50 word' in line.lower():
                        short_desc = line.split(':', 1)[-1].strip()
                    elif 'detailed' in line.lower() or '150 word' in line.lower():
                        long_desc = line.split(':', 1)[-1].strip()
                
                return {
                    'short_description': short_desc or content[:100],
                    'long_description': long_desc or content,
                    'language': language
                }
        
        # Option 2: Groq API
        elif hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                return {
                    'short_description': content[:100],
                    'long_description': content,
                    'language': language
                }
        
        # Fallback: Template-based description
        else:
            if language == 'hi':
                short_desc = f"{product_name} - {material} से बना, {region} की पारंपरिक {style} शैली में।"
                long_desc = f"यह सुंदर {product_name} {region} के कुशल कारीगरों द्वारा {material} का उपयोग करके बनाया गया है। {style} शैली में तैयार यह उत्पाद भारतीय शिल्प कला की समृद्ध परंपरा को दर्शाता है।"
            else:
                short_desc = f"Beautiful {product_name} crafted from {material} in traditional {style} style from {region}."
                long_desc = f"This exquisite {product_name} is handcrafted by skilled artisans from {region} using premium {material}. The {style} style reflects the rich heritage of Indian craftsmanship, making it a perfect addition to your collection."
            
            return {
                'short_description': short_desc,
                'long_description': long_desc,
                'language': language
            }
    
    except Exception as e:
        return {
            'error': str(e),
            'short_description': f"Handcrafted {product_name}",
            'long_description': f"Beautiful {product_name} made with care by Indian artisans.",
            'language': language
        }