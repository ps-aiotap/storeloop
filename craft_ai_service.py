"""
Craft Product Description AI Service
Reuses IndexCopilot.ai's provider system adapted for craft descriptions
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
import os
from dotenv import load_dotenv

from providers.base import BaseLLMProvider
from providers.groq_provider import GroqProvider
from providers.openai_provider import OpenAIProvider
from cache_utils import get_cached_response, cache_response

load_dotenv()
logger = logging.getLogger(__name__)

@dataclass
class ProductContext:
    """Product context for AI generation"""
    name: str
    category: str = ""
    materials: List[str] = None
    origin: str = ""
    style: str = ""
    price_range: str = ""
    target_audience: str = ""
    cultural_significance: str = ""
    
    def __post_init__(self):
        if self.materials is None:
            self.materials = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "materials": self.materials,
            "origin": self.origin,
            "style": self.style,
            "price_range": self.price_range,
            "target_audience": self.target_audience,
            "cultural_significance": self.cultural_significance
        }

class CraftAIService:
    """AI service for generating craft product descriptions"""
    
    def __init__(self):
        self.providers = self._initialize_providers()
        self.fallback_order = ["ollama", "groq", "huggingface", "openai"]
    
    def _initialize_providers(self) -> Dict[str, BaseLLMProvider]:
        """Initialize available LLM providers"""
        providers = {}
        
        # Groq (Free tier)
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            providers["groq"] = GroqProvider(
                api_key=groq_key,
                model="llama3-8b-8192"  # Free tier model
            )
        
        # HuggingFace (Free tier)
        hf_key = os.getenv("HUGGINGFACE_API_KEY")
        if hf_key:
            from providers.huggingface_provider import HuggingFaceProvider
            providers["huggingface"] = HuggingFaceProvider(
                api_key=hf_key,
                model="microsoft/DialoGPT-medium"  # Free tier model
            )
        
        # OpenAI (fallback)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            providers["openai"] = OpenAIProvider(
                api_key=openai_key,
                model="gpt-3.5-turbo"
            )
        
        # Ollama (local, always available)
        try:
            from providers.ollama_provider import OllamaProvider
            providers["ollama"] = OllamaProvider(
                api_key="",  # Not needed for Ollama
                model="llama3.2:3b"
            )
        except ImportError:
            logger.warning("Ollama provider not available")
        
        return providers
    
    def _build_system_prompt(self, language: str = "en") -> str:
        """Build system prompt for craft description generation"""
        if language == "hi":
            return """आप एक विशेषज्ञ शिल्प उत्पाद विवरण लेखक हैं जो भारतीय हस्तशिल्प में विशेषज्ञता रखते हैं।

आपका काम:
- आकर्षक और विस्तृत उत्पाद विवरण लिखना
- सांस्कृतिक संदर्भ और परंपरा को शामिल करना
- ग्राहकों को खरीदने के लिए प्रेरित करना
- शिल्पकार की कुशलता को उजागर करना
- SEO-अनुकूल सामग्री बनाना

शैली: पेशेवर लेकिन गर्मजोशी भरी, सांस्कृतिक रूप से संवेदनशील"""
        else:
            return """You are an expert craft product description writer specializing in Indian handicrafts and artisan products.

Your role:
- Write compelling and detailed product descriptions
- Include cultural context and traditions
- Motivate customers to purchase
- Highlight artisan craftsmanship
- Create SEO-friendly content

Style: Professional yet warm, culturally sensitive, marketing-focused"""
    
    def _build_user_prompt(self, product: ProductContext, language: str = "en") -> str:
        """Build user prompt with product context"""
        context_str = json.dumps(product.to_dict(), indent=2)
        
        if language == "hi":
            return f"""निम्नलिखित उत्पाद के लिए एक आकर्षक विवरण लिखें:

उत्पाद जानकारी:
{context_str}

आवश्यकताएं:
- 80-120 शब्दों में विवरण
- सांस्कृतिक महत्व शामिल करें
- शिल्पकार की कुशलता पर जोर दें
- खरीदारी के लिए प्रेरणादायक भाषा
- केवल विवरण दें, कोई अतिरिक्त टेक्स्ट नहीं"""
        else:
            return f"""Write a compelling product description for the following craft item:

Product Information:
{context_str}

Requirements:
- 80-120 words description
- Include cultural significance
- Emphasize artisan craftsmanship
- Use persuasive language for purchasing
- Provide only the description, no additional text"""
    
    async def generate_description(
        self, 
        product: ProductContext, 
        language: str = "en",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Generate product description using available providers"""
        
        # Check cache first
        if use_cache:
            cached = get_cached_response(
                query=f"craft_description_{language}",
                context_data=product.to_dict(),
                model="multi_provider"
            )
            if cached:
                return {
                    "success": True,
                    "description": cached,
                    "source": "cache",
                    "language": language
                }
        
        # Try providers in fallback order
        for provider_name in self.fallback_order:
            if provider_name not in self.providers:
                continue
                
            try:
                provider = self.providers[provider_name]
                
                # Validate provider config
                if not provider.validate_config():
                    logger.warning(f"{provider_name} provider config invalid")
                    continue
                
                system_prompt = self._build_system_prompt(language)
                user_prompt = self._build_user_prompt(product, language)
                
                logger.info(f"Trying {provider_name} provider")
                
                description = await provider.generate_response(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    timeout=30
                )
                
                if description and len(description.strip()) > 20:
                    # Cache successful response
                    if use_cache:
                        cache_response(
                            query=f"craft_description_{language}",
                            context_data=product.to_dict(),
                            model="multi_provider",
                            response=description,
                            ttl=3600  # 1 hour
                        )
                    
                    return {
                        "success": True,
                        "description": description.strip(),
                        "source": provider_name,
                        "language": language,
                        "model": provider.model
                    }
                    
            except Exception as e:
                logger.error(f"{provider_name} provider failed: {str(e)}")
                continue
        
        # All providers failed - return fallback
        return {
            "success": False,
            "description": self._fallback_description(product, language),
            "source": "fallback",
            "language": language,
            "error": "All AI providers failed"
        }
    
    def _fallback_description(self, product: ProductContext, language: str) -> str:
        """Generate basic fallback description"""
        if language == "hi":
            return f"यह एक सुंदर {product.name} है जो {product.category or 'हस्तशिल्प'} श्रेणी में आता है। यह उत्पाद पारंपरिक भारतीय शिल्पकारी का एक बेहतरीन उदाहरण है और आपके घर या कार्यालय की शोभा बढ़ाएगा।"
        else:
            return f"This beautiful {product.name} is a fine example of traditional Indian craftsmanship in the {product.category or 'handicraft'} category. Handcrafted with care and attention to detail, it makes a perfect addition to your home or office."

# Convenience functions for easy integration
async def generate_craft_description(
    name: str,
    category: str = "",
    materials: List[str] = None,
    origin: str = "",
    style: str = "",
    language: str = "en"
) -> Dict[str, Any]:
    """Convenience function to generate craft description"""
    
    product = ProductContext(
        name=name,
        category=category,
        materials=materials or [],
        origin=origin,
        style=style
    )
    
    service = CraftAIService()
    return await service.generate_description(product, language)

def generate_craft_description_sync(
    name: str,
    category: str = "",
    materials: List[str] = None,
    origin: str = "",
    style: str = "",
    language: str = "en"
) -> Dict[str, Any]:
    """Synchronous wrapper for craft description generation"""
    
    return asyncio.run(generate_craft_description(
        name=name,
        category=category,
        materials=materials,
        origin=origin,
        style=style,
        language=language
    ))

# Demo function
async def demo():
    """Demo the craft AI service"""
    
    test_products = [
        ProductContext(
            name="Handwoven Silk Saree",
            category="Clothing",
            materials=["Silk", "Gold Thread"],
            origin="Varanasi",
            style="Banarasi",
            cultural_significance="Traditional wedding attire"
        ),
        ProductContext(
            name="मिट्टी का दीया",
            category="Home Decor",
            materials=["Clay"],
            origin="Khurja",
            style="Traditional",
            cultural_significance="Festival lighting"
        )
    ]
    
    service = CraftAIService()
    
    for product in test_products:
        language = "hi" if any(ord(char) > 127 for char in product.name) else "en"
        
        print(f"\n📦 Product: {product.name}")
        print("-" * 50)
        
        result = await service.generate_description(product, language)
        
        if result["success"]:
            print(f"✅ Generated via {result['source']}")
            print(f"📝 Description: {result['description']}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            print(f"📝 Fallback: {result['description']}")

if __name__ == "__main__":
    asyncio.run(demo())