import redis
import json
import hashlib
import os
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()

# Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True
)

def generate_cache_key(query: str, context_data: Any, model: str) -> str:
    """Generate a cache key for LLM responses."""
    content = f"{query}:{json.dumps(context_data, sort_keys=True)}:{model}"
    return f"llm_response:{hashlib.md5(content.encode()).hexdigest()}"

def get_cached_response(query: str, context_data: Any, model: str) -> Optional[str]:
    """Get cached LLM response."""
    try:
        cache_key = generate_cache_key(query, context_data, model)
        return redis_client.get(cache_key)
    except Exception:
        return None

def cache_response(query: str, context_data: Any, model: str, response: str, ttl: int = 3600):
    """Cache LLM response with TTL (default 1 hour)."""
    try:
        cache_key = generate_cache_key(query, context_data, model)
        redis_client.setex(cache_key, ttl, response)
    except Exception:
        pass  # Fail silently if caching fails

def clear_cache_pattern(pattern: str = "llm_response:*"):
    """Clear cached responses matching pattern."""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass