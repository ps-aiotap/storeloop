# AI Description Generator Setup

## Quick Start

### 1. Install Ollama (Free Local LLM)

**Windows:**
```bash
# Download from https://ollama.ai/download
# Or use winget
winget install Ollama.Ollama
```

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Install a Model

```bash
# Lightweight model (2GB)
ollama pull llama3.2:3b

# Better quality model (4GB)  
ollama pull mistral:7b

# Code-focused model (4GB)
ollama pull codellama:7b
```

### 3. Start Ollama Server

```bash
ollama serve
```

Server runs on `http://localhost:11434`

### 4. Test the Generator

```bash
cd /path/to/storeloop
python ai_description_generator.py
```

## Configuration Options

### Local Models (Free)
- `llama3.2:3b` - Fast, lightweight (2GB)
- `mistral:7b` - Better quality (4GB)
- `codellama:7b` - Code-focused (4GB)
- `llama3.1:8b` - High quality (4.7GB)

### OpenRouter Fallback (Paid)
- `mistralai/mixtral-8x7b-instruct` - $0.0006/1K tokens
- `nousresearch/nous-hermes-2-mixtral-8x7b-dpo` - $0.0008/1K tokens
- `meta-llama/llama-3.1-8b-instruct` - $0.0002/1K tokens

## Integration with StoreLoop

```python
# In stores/ai_service.py
from ai_description_generator import AIDescriptionGenerator, AIConfig

config = AIConfig(
    ollama_model="llama3.2:3b",
    openrouter_key=os.environ.get("OPENROUTER_KEY", "")
)

generator = AIDescriptionGenerator(config)

def generate_product_description(product_name, category, language="en"):
    return generator.generate_description(product_name, category, language)
```

## Cost Comparison

| Service | Cost | Quality | Speed |
|---------|------|---------|-------|
| Ollama (Local) | **FREE** | Good | Fast |
| OpenRouter Mixtral | $0.60/1M tokens | Excellent | Medium |
| OpenAI GPT-4 | $30/1M tokens | Excellent | Fast |

## Troubleshooting

### Ollama Not Starting
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart service
ollama serve
```

### Model Not Found
```bash
# List installed models
ollama list

# Pull missing model
ollama pull llama3.2:3b
```

### Connection Errors
- Check firewall settings
- Ensure port 11434 is open
- Try `http://127.0.0.1:11434` instead of localhost

## Performance Tips

1. **Use smaller models for development** (`llama3.2:3b`)
2. **Use larger models for production** (`mistral:7b`)
3. **Enable GPU acceleration** if available
4. **Adjust timeout based on model size**

## Example Output

```
📦 Product: Handwoven Silk Saree (Clothing) - Language: en
------------------------------------------------------------
✅ Success via Ollama
📝 Description: This exquisite handwoven silk saree showcases traditional Indian craftsmanship with intricate patterns and vibrant colors. Perfect for weddings and special occasions, it combines elegance with cultural heritage. Made from premium silk threads, ensuring comfort and durability.
⏱️ Response time: 2.34s
🔢 Tokens used: 67

📦 Product: मिट्टी का दीया (Home Decor) - Language: hi  
------------------------------------------------------------
✅ Success via Ollama
📝 Description: यह पारंपरिक मिट्टी का दीया हस्तनिर्मित है और त्योहारों के लिए आदर्श है। इसकी प्राकृतिक मिट्टी की सुगंध और सुंदर डिज़ाइन आपके घर में दिव्य प्रकाश फैलाता है। पर्यावरण-अनुकूल और टिकाऊ।
⏱️ Response time: 1.87s
🔢 Tokens used: 89
```