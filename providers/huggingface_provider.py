import aiohttp
import asyncio
import logging
from typing import Dict, Any
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)

class HuggingFaceProvider(BaseLLMProvider):
    """Hugging Face Inference API provider (free tier)"""
    
    def __init__(self, api_key: str, model: str = "microsoft/DialoGPT-medium"):
        super().__init__(api_key, model)
        self.base_url = "https://api-inference.huggingface.co/models"
        self.endpoint = f"{self.base_url}/{model}"
    
    async def generate_response(self, system_prompt: str, user_prompt: str, timeout: int = 30) -> str:
        """Generate response using Hugging Face Inference API"""
        
        # Combine prompts for text generation
        combined_prompt = f"{system_prompt}\n\n{user_prompt}\n\nResponse:"
        
        payload = {
            "inputs": combined_prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.post(self.endpoint, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Handle different response formats
                        if isinstance(data, list) and len(data) > 0:
                            generated_text = data[0].get("generated_text", "")
                        elif isinstance(data, dict):
                            generated_text = data.get("generated_text", "")
                        else:
                            generated_text = str(data)
                        
                        return generated_text.strip()
                    else:
                        error_text = await response.text()
                        raise Exception(f"HuggingFace API error {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            raise Exception("HuggingFace request timeout")
        except aiohttp.ClientError as e:
            raise Exception(f"HuggingFace connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"HuggingFace error: {str(e)}")
    
    def validate_config(self) -> bool:
        """Validate HuggingFace configuration"""
        return bool(self.api_key and len(self.api_key) > 10)