from .openai_provider import OpenAIProvider
from .groq_provider import GroqProvider
from .base import BaseLLMProvider

PROVIDERS = {
    "openai": OpenAIProvider,
    "groq": GroqProvider,
}