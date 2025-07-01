#!/usr/bin/env python3
"""
AI Product Description Generator
Supports local Ollama and fallback to OpenRouter with retry logic
"""

import requests
import time
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIConfig:
    # Local Ollama settings
    ollama_url: str = "http://localhost:11434/v1/chat/completions"
    ollama_model: str = "llama3.2:3b"  # or "mistral:7b", "codellama:7b"
    
    # OpenRouter fallback settings
    openrouter_url: str = "https://openrouter.ai/api/v1/chat/completions"
    openrouter_key: str = ""  # Set your API key here
    openrouter_model: str = "mistralai/mixtral-8x7b-instruct"  # or "nousresearch/nous-hermes-2-mixtral-8x7b-dpo"
    
    # Request settings
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

class AIDescriptionGenerator:
    def __init__(self, config: AIConfig = None):
        self.config = config or AIConfig()
    
    def generate_description(self, product_title: str, category: str, language: str = "en") -> Dict[str, Any]:
        """Generate product description with local LLM first, fallback to OpenRouter"""
        
        # Try local Ollama first
        result = self._try_local_llm(product_title, category, language)
        if result['success']:
            logger.info("✅ Generated description using local Ollama")
            return result
        
        # Fallback to OpenRouter
        logger.warning("⚠️ Local LLM failed, trying OpenRouter fallback")
        result = self._try_openrouter(product_title, category, language)
        if result['success']:
            logger.info("✅ Generated description using OpenRouter")
            return result
        
        # Both failed
        logger.error("❌ Both local and remote AI services failed")
        return {
            'success': False,
            'error': 'All AI services unavailable',
            'description': self._fallback_description(product_title, category, language)
        }
    
    def _try_local_llm(self, product_title: str, category: str, language: str) -> Dict[str, Any]:
        """Try local Ollama LLM"""
        try:
            prompt = self._build_prompt(product_title, category, language)
            
            payload = {
                "model": self.config.ollama_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 200
            }
            
            return self._make_request(self.config.ollama_url, payload, headers={}, service="Ollama")
            
        except Exception as e:
            logger.error(f"Local LLM error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _try_openrouter(self, product_title: str, category: str, language: str) -> Dict[str, Any]:
        """Try OpenRouter as fallback"""
        if not self.config.openrouter_key:
            return {'success': False, 'error': 'OpenRouter API key not configured'}
        
        try:
            prompt = self._build_prompt(product_title, category, language)
            
            payload = {
                "model": self.config.openrouter_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 200
            }
            
            headers = {
                "Authorization": f"Bearer {self.config.openrouter_key}",
                "Content-Type": "application/json"
            }
            
            return self._make_request(self.config.openrouter_url, payload, headers, service="OpenRouter")
            
        except Exception as e:
            logger.error(f"OpenRouter error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _make_request(self, url: str, payload: dict, headers: dict, service: str) -> Dict[str, Any]:
        """Make API request with retry logic"""
        
        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"🔄 Attempting {service} request (attempt {attempt + 1}/{self.config.max_retries})")
                
                start_time = time.time()
                response = requests.post(
                    url, 
                    json=payload, 
                    headers=headers, 
                    timeout=self.config.timeout
                )
                response_time = time.time() - start_time
                
                logger.info(f"⏱️ {service} response time: {response_time:.2f}s")
                
                if response.status_code == 200:
                    data = response.json()
                    description = data['choices'][0]['message']['content'].strip()
                    
                    return {
                        'success': True,
                        'description': description,
                        'service': service,
                        'model': payload['model'],
                        'response_time': response_time,
                        'tokens_used': data.get('usage', {}).get('total_tokens', 0)
                    }
                else:
                    logger.warning(f"⚠️ {service} HTTP {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"⏰ {service} timeout (attempt {attempt + 1})")
            except requests.exceptions.ConnectionError:
                logger.warning(f"🔌 {service} connection error (attempt {attempt + 1})")
            except Exception as e:
                logger.error(f"❌ {service} unexpected error: {str(e)}")
            
            # Wait before retry (except last attempt)
            if attempt < self.config.max_retries - 1:
                time.sleep(self.config.retry_delay * (attempt + 1))  # Exponential backoff
        
        return {'success': False, 'error': f'{service} failed after {self.config.max_retries} attempts'}
    
    def _build_prompt(self, product_title: str, category: str, language: str) -> str:
        """Build AI prompt for product description"""
        
        if language == "hi":
            return f"""आप एक ई-कॉमर्स प्रोडक्ट डिस्क्रिप्शन एक्सपर्ट हैं। 

प्रोडक्ट: {product_title}
कैटेगरी: {category}

कृपया इस प्रोडक्ट के लिए एक आकर्षक और विस्तृत विवरण लिखें जो:
- ग्राहकों को खरीदने के लिए प्रेरित करे
- प्रोडक्ट की विशेषताओं को हाइलाइट करे  
- भारतीय ग्राहकों के लिए उपयुक्त हो
- 50-80 शब्दों में हो

केवल विवरण दें, कोई अतिरिक्त टेक्स्ट नहीं।"""
        else:
            return f"""You are an e-commerce product description expert.

Product: {product_title}
Category: {category}

Please write an engaging and detailed product description that:
- Motivates customers to purchase
- Highlights key product features
- Appeals to Indian customers
- Is 50-80 words long

Provide only the description, no additional text."""
    
    def _fallback_description(self, product_title: str, category: str, language: str) -> str:
        """Generate basic fallback description when AI fails"""
        if language == "hi":
            return f"यह एक उच्च गुणवत्ता का {product_title} है जो {category} श्रेणी में आता है। यह उत्पाद भारतीय ग्राहकों की जरूरतों को ध्यान में रखकर बनाया गया है।"
        else:
            return f"This is a high-quality {product_title} in the {category} category. This product is designed keeping Indian customers' needs in mind."

def main():
    """Demo the AI description generator"""
    
    # Configure (set your OpenRouter key if you have one)
    config = AIConfig(
        openrouter_key="",  # Add your key here for fallback
        ollama_model="llama3.2:3b"  # Change based on your Ollama setup
    )
    
    generator = AIDescriptionGenerator(config)
    
    # Test cases
    test_products = [
        ("Handwoven Silk Saree", "Clothing", "en"),
        ("मिट्टी का दीया", "Home Decor", "hi"),
        ("Kashmiri Pashmina Shawl", "Accessories", "en"),
        ("हस्तनिर्मित लकड़ी की मूर्ति", "Art & Crafts", "hi")
    ]
    
    print("🚀 AI Product Description Generator Demo\n")
    
    for title, category, language in test_products:
        print(f"📦 Product: {title} ({category}) - Language: {language}")
        print("-" * 60)
        
        result = generator.generate_description(title, category, language)
        
        if result['success']:
            print(f"✅ Success via {result.get('service', 'Unknown')}")
            print(f"📝 Description: {result['description']}")
            if 'response_time' in result:
                print(f"⏱️ Response time: {result['response_time']:.2f}s")
            if 'tokens_used' in result:
                print(f"🔢 Tokens used: {result['tokens_used']}")
        else:
            print(f"❌ Failed: {result['error']}")
            print(f"📝 Fallback: {result.get('description', 'No fallback available')}")
        
        print("\n")

if __name__ == "__main__":
    main()