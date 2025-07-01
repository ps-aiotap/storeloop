"""Mock services for demo purposes - simulate WhatsApp and AI without API costs"""

import random
import time
from typing import Dict, Any

class MockWhatsAppService:
    """Mock WhatsApp service for demo - shows what real integration would look like"""
    
    @staticmethod
    def send_notification(phone: str, message: str, template_type: str = 'order_confirmation') -> Dict[str, Any]:
        """Simulate WhatsApp message sending"""
        # Simulate API delay
        time.sleep(0.5)
        
        # Simulate success/failure (95% success rate)
        success = random.random() > 0.05
        
        if success:
            return {
                'success': True,
                'message_id': f'wamid.{random.randint(100000, 999999)}',
                'status': 'sent',
                'phone': phone,
                'template': template_type,
                'timestamp': int(time.time())
            }
        else:
            return {
                'success': False,
                'error': 'Failed to deliver message',
                'phone': phone,
                'template': template_type,
                'timestamp': int(time.time())
            }

class MockAIService:
    """Mock AI service for demo - generates realistic product descriptions"""
    
    HINDI_TEMPLATES = [
        "यह एक सुंदर हस्तनिर्मित {product_name} है जो {material} से बना है। {region} की पारंपरिक {style} शैली में तैयार किया गया है।",
        "प्रामाणिक {region} शिल्पकारी का यह {product_name} {material} से निर्मित है। {style} डिज़ाइन के साथ यह अनूठा और आकर्षक है।",
        "हस्तकला की इस अद्भुत कृति {product_name} को {material} से बनाया गया है। {region} की {style} परंपरा को दर्शाता है।"
    ]
    
    ENGLISH_TEMPLATES = [
        "This beautiful handcrafted {product_name} is made from {material}. Created in the traditional {style} style of {region}.",
        "An authentic {region} crafted {product_name} made from {material}. Features {style} design that is unique and attractive.",
        "This exquisite handmade {product_name} is crafted from {material}. Represents the {style} tradition of {region}."
    ]
    
    @staticmethod
    def generate_description(product_name: str, material: str, region: str, style: str, language: str = 'en') -> Dict[str, Any]:
        """Generate mock AI description"""
        # Simulate API delay
        time.sleep(1.0)
        
        # Simulate occasional failures (10% failure rate)
        if random.random() < 0.1:
            return {
                'success': False,
                'error': 'AI service temporarily unavailable',
                'language': language
            }
        
        # Select template based on language
        if language == 'hi':
            template = random.choice(MockAIService.HINDI_TEMPLATES)
        else:
            template = random.choice(MockAIService.ENGLISH_TEMPLATES)
        
        # Generate description
        description = template.format(
            product_name=product_name or 'उत्पाद' if language == 'hi' else 'product',
            material=material or 'सामग्री' if language == 'hi' else 'material',
            region=region or 'भारत' if language == 'hi' else 'India',
            style=style or 'पारंपरिक' if language == 'hi' else 'traditional'
        )
        
        # Add some variation
        if language == 'hi':
            description += f" इसकी गुणवत्ता और शिल्पकारी अद्वितीय है।"
        else:
            description += f" The quality and craftsmanship are exceptional."
        
        return {
            'success': True,
            'description': description,
            'language': language,
            'confidence': random.uniform(0.85, 0.98),
            'tokens_used': len(description.split()) * 2  # Mock token count
        }

class MockImageValidator:
    """Mock image URL validation service"""
    
    VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    
    @staticmethod
    def validate_image_url(url: str) -> Dict[str, Any]:
        """Validate image URL without making actual HTTP requests"""
        if not url:
            return {
                'valid': False,
                'error': 'URL is empty',
                'url': url
            }
        
        # Check if URL looks like an image
        url_lower = url.lower()
        has_valid_extension = any(url_lower.endswith(ext) for ext in MockImageValidator.VALID_EXTENSIONS)
        
        # Mock validation results
        if 'example.com' in url or 'placeholder' in url:
            return {
                'valid': False,
                'error': 'Placeholder or example URL detected',
                'url': url
            }
        
        if not has_valid_extension:
            return {
                'valid': False,
                'error': 'Invalid image format. Supported: JPG, PNG, WebP, GIF',
                'url': url
            }
        
        # Simulate network check (90% success rate)
        if random.random() > 0.9:
            return {
                'valid': False,
                'error': 'Image URL not accessible',
                'url': url
            }
        
        return {
            'valid': True,
            'url': url,
            'format': url_lower.split('.')[-1],
            'estimated_size': f"{random.randint(50, 500)}KB"
        }