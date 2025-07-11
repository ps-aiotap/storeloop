import random
from datetime import datetime, timedelta
from typing import List, Dict
from ..models import CustomerProfile, Interaction
from ..utils.mode_context import get_crm_mode

class MockMessageConnector:
    """Mock message connector for testing channel integrations"""
    
    def __init__(self):
        self.mode = get_crm_mode().lower()
    
    def generate_mock_interactions(self, customer: CustomerProfile, count: int = 5) -> List[Interaction]:
        """Generate mock interactions for a customer"""
        interactions = []
        
        if self.mode == 'storeloop':
            messages = self._get_storeloop_messages()
            channels = ['whatsapp', 'phone', 'email']
        else:
            messages = self._get_aiotap_messages()
            channels = ['email', 'upwork', 'phone']
        
        for i in range(count):
            # Alternate between inbound and outbound
            direction = 'inbound' if i % 2 == 0 else 'outbound'
            channel = random.choice(channels)
            
            # Select appropriate message based on direction
            message_pool = messages[direction]
            message_template = random.choice(message_pool)
            
            # Safe formatting - only replace if placeholder exists
            content = message_template
            if '{customer_name}' in content:
                content = content.replace('{customer_name}', customer.name)
            if '{company}' in content:
                content = content.replace('{company}', customer.company or "your company")
            if '{product_type}' in content:
                content = content.replace('{product_type}', random.choice(['jewelry', 'pottery', 'textiles', 'crafts']))
            
            # Create interaction with realistic timestamp
            created_at = datetime.now() - timedelta(days=random.randint(1, 30))
            
            interaction = Interaction(
                customer=customer,
                channel=channel,
                direction=direction,
                content=content,
                created_at=created_at
            )
            interactions.append(interaction)
        
        return interactions
    
    def _get_storeloop_messages(self) -> Dict[str, List[str]]:
        """Mock messages for StoreLoop artisan customers"""
        return {
            'inbound': [
                "Hi, I saw your beautiful {product_type} on WhatsApp. Is it still available?",
                "Hello, can you tell me more about the handmade jewelry collection?",
                "I'm interested in ordering a custom saree. What's the process?",
                "Do you have any pottery items in stock? I need them for a gift.",
                "Can you send me photos of your latest craft items?",
                "What's the price for the embroidered shawl I saw earlier?",
                "I'd like to place an order for 3 clay diyas. How much would that be?",
                "Is delivery available to Mumbai? How long does it take?"
            ],
            'outbound': [
                "Hello {customer_name}! Thank you for your interest in our handcrafted items.",
                "Hi! Yes, the {product_type} is available. Here are some photos.",
                "Thank you for your order! We'll start working on your custom piece right away.",
                "Your order has been shipped and should reach you in 3-4 days.",
                "We have new arrivals in our jewelry collection. Would you like to see them?",
                "Hello! Just checking if you received your order safely.",
                "We're offering a 10% discount on all pottery items this week!",
                "Thank you for choosing our handmade products. Your support means a lot!"
            ]
        }
    
    def _get_aiotap_messages(self) -> Dict[str, List[str]]:
        """Mock messages for AioTap consulting leads"""
        return {
            'inbound': [
                "Hi, I'm looking for AI consulting services for my startup. Can we discuss?",
                "We need help implementing machine learning in our e-commerce platform.",
                "I saw your profile on Upwork. Can you help with our chatbot project?",
                "Our company wants to explore AI automation. What's your approach?",
                "Do you have experience with computer vision projects?",
                "We're looking for someone to help with our data science strategy.",
                "Can you provide a quote for an AI-powered recommendation system?",
                "I'd like to schedule a consultation call to discuss our AI needs."
            ],
            'outbound': [
                "Hi {customer_name}, thanks for reaching out about AI consulting!",
                "I'd be happy to discuss your machine learning requirements.",
                "Based on your project description, I think we can definitely help with that.",
                "I've sent you a proposal for the AI automation project we discussed.",
                "Let's schedule a call to dive deeper into your technical requirements.",
                "I have experience with similar projects at {company}. Here's what we can do...",
                "Thanks for the detailed brief. I'll prepare a custom solution for you.",
                "Following up on our conversation - do you have any questions about the proposal?"
            ]
        }
    
    def simulate_whatsapp_webhook(self, customer_id: int, message: str) -> Dict:
        """Simulate WhatsApp webhook payload"""
        return {
            'from': f'+91{random.randint(7000000000, 9999999999)}',
            'to': '+919876543210',
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'message_id': f'wamid.{random.randint(100000, 999999)}',
            'customer_id': customer_id
        }
    
    def simulate_email_webhook(self, customer_id: int, subject: str, body: str) -> Dict:
        """Simulate email webhook payload"""
        return {
            'from': f'customer{customer_id}@example.com',
            'to': 'hello@aiotap.com',
            'subject': subject,
            'body': body,
            'timestamp': datetime.now().isoformat(),
            'message_id': f'email_{random.randint(100000, 999999)}',
            'customer_id': customer_id
        }

# Global instance
mock_connector = MockMessageConnector()