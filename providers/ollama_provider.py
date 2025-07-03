import aiohttp
import asyncio
import logging
from typing import Dict, Any
from .base import BaseLLMProvider

logger = logging.getLogger(__name__)

class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, api_key: str, model: str, base_url: str = "http://localhost:11434"):
        super().__init__(api_key, model)
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/generate"
    
    async def generate_response(self, system_prompt: str, user_prompt: str, timeout: int = 30) -> str:
        """Generate response using Ollama API"""
        
        # Combine system and user prompts for Ollama
        combined_prompt = f"{system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
        
        payload = {
            "model": self.model,
            "prompt": combined_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 200
            }
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.post(self.endpoint, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "").strip()
                    else:
                        error_text = await response.text()
                        raise Exception(f"Ollama API error {response.status}: {error_text}")
                        
        except asyncio.TimeoutError:
            raise Exception("Ollama request timeout")
        except aiohttp.ClientError as e:
            raise Exception(f"Ollama connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")
    
    def validate_config(self) -> bool:
        """Validate Ollama configuration"""
        try:
            # Check if Ollama server is running
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False