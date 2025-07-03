from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union

class BaseLLMProvider(ABC):
    """Base class for LLM providers."""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def generate_response(self, system_prompt: str, user_prompt: str, timeout: int = 30) -> str:
        """Generate response from the LLM provider."""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration."""
        pass