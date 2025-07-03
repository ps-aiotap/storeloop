import requests
from .base import BaseLLMProvider

class GroqProvider(BaseLLMProvider):
    """Groq provider implementation."""
    
    async def generate_response(self, system_prompt: str, user_prompt: str, timeout: int = 30) -> str:
        if not self.api_key:
            return "Error: Groq API key not found"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 800
        }
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=timeout
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Groq API Error: {response.status_code}"
        except Exception as e:
            return f"Groq API Error: {str(e)}"
    
    def validate_config(self) -> bool:
        return bool(self.api_key)