"""
FastAPI service for craft description generation
Async processing with multiple LLM providers
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import logging
from datetime import datetime
import uuid

from craft_ai_service import CraftAIService, ProductContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Craft AI Description Service",
    description="AI-powered product description generation for Indian crafts",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global AI service instance
ai_service = CraftAIService()

# Request/Response models
class ProductRequest(BaseModel):
    name: str
    category: Optional[str] = ""
    materials: Optional[List[str]] = []
    origin: Optional[str] = ""
    style: Optional[str] = ""
    price_range: Optional[str] = ""
    target_audience: Optional[str] = ""
    cultural_significance: Optional[str] = ""
    language: Optional[str] = "en"
    use_cache: Optional[bool] = True

class BatchProductRequest(BaseModel):
    products: List[ProductRequest]
    language: Optional[str] = "en"
    use_cache: Optional[bool] = True

class DescriptionResponse(BaseModel):
    success: bool
    description: str
    source: str
    language: str
    model: Optional[str] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None

class BatchResponse(BaseModel):
    total: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]
    processing_time: float

# In-memory task storage (use Redis in production)
task_storage: Dict[str, Dict[str, Any]] = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Craft AI Description Service",
        "status": "running",
        "providers": list(ai_service.providers.keys()),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    provider_status = {}
    
    for name, provider in ai_service.providers.items():
        try:
            is_valid = provider.validate_config()
            provider_status[name] = {
                "available": is_valid,
                "model": provider.model
            }
        except Exception as e:
            provider_status[name] = {
                "available": False,
                "error": str(e)
            }
    
    return {
        "status": "healthy",
        "providers": provider_status,
        "cache_enabled": True,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/generate", response_model=DescriptionResponse)
async def generate_description(request: ProductRequest):
    """Generate single product description"""
    
    start_time = datetime.now()
    
    try:
        # Create product context
        product = ProductContext(
            name=request.name,
            category=request.category,
            materials=request.materials,
            origin=request.origin,
            style=request.style,
            price_range=request.price_range,
            target_audience=request.target_audience,
            cultural_significance=request.cultural_significance
        )
        
        # Generate description
        result = await ai_service.generate_description(
            product=product,
            language=request.language,
            use_cache=request.use_cache
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return DescriptionResponse(
            success=result["success"],
            description=result["description"],
            source=result["source"],
            language=result["language"],
            model=result.get("model"),
            error=result.get("error"),
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error generating description: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/batch")
async def generate_batch_descriptions(request: BatchProductRequest):
    """Generate descriptions for multiple products"""
    
    task_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    # Store initial task status
    task_storage[task_id] = {
        "status": "processing",
        "total": len(request.products),
        "completed": 0,
        "results": [],
        "start_time": start_time.isoformat()
    }
    
    try:
        # Process all products concurrently
        tasks = []
        for product_req in request.products:
            product = ProductContext(
                name=product_req.name,
                category=product_req.category,
                materials=product_req.materials,
                origin=product_req.origin,
                style=product_req.style,
                price_range=product_req.price_range,
                target_audience=product_req.target_audience,
                cultural_significance=product_req.cultural_significance
            )
            
            task = ai_service.generate_description(
                product=product,
                language=product_req.language or request.language,
                use_cache=request.use_cache
            )\n            tasks.append(task)\n        \n        # Execute all tasks concurrently\n        results = await asyncio.gather(*tasks, return_exceptions=True)\n        \n        # Process results\n        successful = 0\n        failed = 0\n        processed_results = []\n        \n        for i, result in enumerate(results):\n            if isinstance(result, Exception):\n                processed_results.append({\n                    \"product_name\": request.products[i].name,\n                    \"success\": False,\n                    \"error\": str(result)\n                })\n                failed += 1\n            else:\n                processed_results.append({\n                    \"product_name\": request.products[i].name,\n                    \"success\": result[\"success\"],\n                    \"description\": result[\"description\"],\n                    \"source\": result[\"source\"],\n                    \"language\": result[\"language\"],\n                    \"model\": result.get(\"model\")\n                })\n                if result[\"success\"]:\n                    successful += 1\n                else:\n                    failed += 1\n        \n        processing_time = (datetime.now() - start_time).total_seconds()\n        \n        # Update task storage\n        task_storage[task_id] = {\n            \"status\": \"completed\",\n            \"total\": len(request.products),\n            \"successful\": successful,\n            \"failed\": failed,\n            \"results\": processed_results,\n            \"processing_time\": processing_time,\n            \"completed_at\": datetime.now().isoformat()\n        }\n        \n        return BatchResponse(\n            total=len(request.products),\n            successful=successful,\n            failed=failed,\n            results=processed_results,\n            processing_time=processing_time\n        )\n        \n    except Exception as e:\n        logger.error(f\"Error in batch processing: {str(e)}\")\n        task_storage[task_id][\"status\"] = \"failed\"\n        task_storage[task_id][\"error\"] = str(e)\n        raise HTTPException(status_code=500, detail=str(e))\n\n@app.get(\"/task/{task_id}\")\nasync def get_task_status(task_id: str):\n    \"\"\"Get batch processing task status\"\"\"\n    \n    if task_id not in task_storage:\n        raise HTTPException(status_code=404, detail=\"Task not found\")\n    \n    return task_storage[task_id]\n\n@app.delete(\"/cache\")\nasync def clear_cache():\n    \"\"\"Clear AI response cache\"\"\"\n    try:\n        from cache_utils import clear_cache_pattern\n        clear_cache_pattern(\"llm_response:*\")\n        return {\"message\": \"Cache cleared successfully\"}\n    except Exception as e:\n        raise HTTPException(status_code=500, detail=f\"Failed to clear cache: {str(e)}\")\n\n@app.get(\"/providers\")\nasync def list_providers():\n    \"\"\"List available AI providers and their status\"\"\"\n    \n    provider_info = {}\n    \n    for name, provider in ai_service.providers.items():\n        try:\n            is_available = provider.validate_config()\n            provider_info[name] = {\n                \"available\": is_available,\n                \"model\": provider.model,\n                \"type\": provider.__class__.__name__\n            }\n        except Exception as e:\n            provider_info[name] = {\n                \"available\": False,\n                \"error\": str(e),\n                \"model\": provider.model,\n                \"type\": provider.__class__.__name__\n            }\n    \n    return {\n        \"providers\": provider_info,\n        \"fallback_order\": ai_service.fallback_order\n    }\n\nif __name__ == \"__main__\":\n    import uvicorn\n    uvicorn.run(app, host=\"0.0.0.0\", port=8001)