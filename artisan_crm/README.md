# Artisan CRM - AI-Powered Customer Relationship Management

A modular, AI-powered CRM system built for both StoreLoop (artisan e-commerce) and AioTap (AI consulting) businesses.

## Features

### 🤖 AI-Powered Workflows
- **Conversation Summarization**: AI-generated customer summaries using LangChain
- **Reply Suggestions**: Context-aware reply recommendations
- **Intent Classification**: Automatic message intent detection
- **Follow-up Generation**: AI-powered follow-up recommendations

### 📊 Customer Management
- **Customer Profiles**: Comprehensive customer information with interaction history
- **Interaction Timeline**: Complete conversation history across channels
- **Tag Management**: Flexible customer categorization
- **Lead Scoring**: Automated lead scoring and prioritization

### 🎯 Lead Pipeline
- **Kanban Board**: Drag-and-drop lead management
- **Stage Tracking**: Customizable pipeline stages per mode
- **Progress Monitoring**: Visual pipeline analytics

### 🔄 Mode-Aware Operation
- **StoreLoop Mode**: Optimized for artisan WhatsApp sales
- **AioTap Mode**: Tailored for AI consulting workflows
- **Dynamic UI**: Mode-specific templates and workflows

## Architecture

### Database Design
- **Separate Database**: Uses `artisan_crm` PostgreSQL database
- **Cross-Database Integration**: Links to StoreLoop users via ID references
- **Database Router**: Automatic routing for CRM models

### AI Integration
- **Model Context Protocol (MCP)**: Structured AI context management
- **LangChain Pipeline**: Modular AI workflow processing
- **Mock Connectors**: Development-friendly channel simulation

## Quick Start

### 1. Seed Sample Data
```bash
# For StoreLoop mode (default)
python manage.py seed_crm_data --customers 10

# For AioTap mode
CRM_MODE=AIO python manage.py seed_crm_data --customers 10
```

### 2. Generate AI Follow-ups
```bash
python manage.py generate_followups --days 7 --limit 20
```

### 3. Access CRM Interface
- **Customer List**: http://localhost:8000/crm/
- **Lead Pipeline**: http://localhost:8000/crm/pipeline/
- **Admin Interface**: http://localhost:8000/admin/

## API Endpoints

### Customer Management
- `GET /crm/customers/` - Customer list with filters
- `GET /crm/customers/<id>/` - Customer detail with timeline
- `POST /crm/customers/<id>/interaction/` - Add interaction

### AI Features
- `POST /crm/customers/<id>/summary/` - Generate AI summary
- `POST /crm/customers/<id>/reply/` - Get reply suggestion

### Pipeline Management
- `GET /crm/pipeline/` - Kanban pipeline view
- `POST /crm/pipeline/move/` - Move lead between stages

## Mode Configuration

### Environment Variables
```bash
# StoreLoop Mode (default)
CRM_MODE=STORELOOP

# AioTap Mode
CRM_MODE=AIO

# Database
CRM_DB_NAME=artisan_crm

# AI Integration
OPENAI_API_KEY=your-openai-key
```

### Mode-Specific Features

#### StoreLoop Mode
- WhatsApp-focused channels
- Artisan-friendly terminology
- Product inquiry workflows
- Hindi/English support

#### AioTap Mode
- Email/Upwork channels
- B2B consulting terminology
- Project-based workflows
- Technical proposal tracking

## Development

### Mock Channel Integration
The system includes mock message connectors for testing:

```python
from artisan_crm.integrations.mock_channels import mock_connector

# Generate mock interactions
interactions = mock_connector.generate_mock_interactions(customer, count=5)
```

### Custom AI Pipelines
Extend the LangChain pipeline:

```python
from artisan_crm.context.context_protocol import ConversationContext
from artisan_crm.langchain_pipeline import crm_ai

context = ConversationContext(
    customer_name="John Doe",
    interaction_history=["Hello", "How can I help?"],
    # ... other fields
)

summary = crm_ai.summarize_conversation(context)
```

## Testing

The system includes comprehensive test data and mock integrations:

- **48 Test Scenarios**: Covers all major workflows
- **Mock Channels**: WhatsApp, Email, Upwork simulation
- **AI Mocking**: Development-friendly AI responses
- **Cross-Mode Testing**: Both StoreLoop and AioTap scenarios

## Future Enhancements

- **Real Channel Integration**: WhatsApp Business API, Email providers
- **Advanced AI**: Custom model fine-tuning
- **Analytics Dashboard**: Conversion tracking and insights
- **Mobile App**: Native mobile CRM interface
- **Enterprise Features**: Multi-tenant support, advanced permissions