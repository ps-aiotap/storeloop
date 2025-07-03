import openai
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider implementation."""
    
    async def generate_response(self, system_prompt: str, user_prompt: str, timeout: int = 30) -> str:
        if not self.api_key:
            return "Error: OpenAI API key not found"
        
        client = openai.OpenAI(api_key=self.api_key, timeout=timeout)
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"
    
    def validate_config(self) -> bool:
        return bool(self.api_key)