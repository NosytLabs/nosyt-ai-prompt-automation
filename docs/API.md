# 🔧 Nosyt AI API Reference

**Complete API documentation for the Nosyt AI Prompt Automation System**

---

## 🌐 Web Interface Endpoints

### Dashboard
```http
GET /
```
**Description**: Main dashboard with real-time analytics
**Response**: HTML dashboard page

### Health Check
```http
GET /health
```
**Response**:
```json
{
    "status": "healthy",
    "timestamp": "2025-08-04T12:00:00Z",
    "system": "Nosyt AI Prompt Automation",
    "version": "1.0.0"
}
```

---

## 📊 Analytics Endpoints

### Daily Analytics
```http
GET /api/analytics/daily
```
**Response**:
```json
{
    "date": "2025-08-04",
    "products_created": 15,
    "daily_revenue": 450.00,
    "daily_sales": 12,
    "avg_quality_score": 0.87,
    "top_niche": "Business & Marketing",
    "conversion_rate": 80.0
}
```

### Weekly Analytics
```http
GET /api/analytics/weekly
```
**Response**:
```json
{
    "period": "7_days",
    "total_products": 105,
    "total_revenue": 3150.00,
    "total_sales": 84,
    "avg_quality_score": 0.85,
    "conversion_rate": 80.0,
    "top_niches": [
        {
            "niche": "Business & Marketing",
            "count": 25,
            "avg_quality": 0.88
        }
    ],
    "daily_trends": [
        {
            "date": "2025-08-04",
            "products": 15,
            "quality": 0.87
        }
    ]
}
```

### Revenue Metrics
```http
GET /api/revenue
```
**Response**:
```json
{
    "total_products": 500,
    "total_revenue": 15750.00,
    "total_sales": 420,
    "avg_quality_score": 0.86,
    "monthly_revenue": [
        {
            "month": "2025-08",
            "revenue": 3150.00,
            "sales": 84
        }
    ],
    "top_products": [
        {
            "title": "Advanced Marketing Strategy Prompts",
            "niche": "Business & Marketing",
            "price": 45.00,
            "sales_count": 15,
            "total_revenue": 675.00
        }
    ]
}
```

### Niche Performance
```http
GET /api/niches
```
**Response**:
```json
{
    "niche_performance": [
        {
            "niche": "Business & Marketing",
            "products_count": 125,
            "avg_quality_score": 0.88,
            "avg_price": 42.50,
            "total_sales": 105,
            "total_revenue": 4462.50,
            "conversion_rate": 84.0
        }
    ]
}
```

### Revenue Prediction
```http
GET /api/prediction/{days}
```
**Parameters**:
- `days` (int): Number of days to predict ahead

**Response**:
```json
{
    "prediction_period_days": 30,
    "historical_avg_daily_revenue": 150.00,
    "predicted_total_revenue": 4650.00,
    "confidence": "medium"
}
```

---

## 🤖 Generation Endpoints

### Trigger Manual Generation
```http
POST /api/generate
```
**Description**: Manually trigger prompt generation cycle
**Response**:
```json
{
    "status": "success",
    "message": "Generation started"
}
```

---

## 🐍 Python API Classes

### PromptGenerator

#### Initialize
```python
from prompt_generator import PromptGenerator
from config import Config

config = Config()
generator = PromptGenerator(config)
await generator.initialize()
```

#### Generate Daily Batch
```python
prompts = await generator.generate_daily_batch()
# Returns List[Dict] with prompt data
```

#### Generate Niche Prompts
```python
niche_prompts = await generator.generate_niche_prompts(
    niche="Business & Marketing",
    count=5
)
```

### WhopIntegration

#### Initialize
```python
from whop_integration import WhopIntegration

whop = WhopIntegration(config)
await whop.initialize()
```

#### Create Products
```python
product_ids = await whop.create_products(prompts, marketing_content)
# Returns List[str] of product IDs
```

#### Get Product Stats
```python
stats = await whop.get_product_stats(product_id)
# Returns Dict with views, sales, revenue, conversion_rate
```

### AnalyticsTracker

#### Initialize
```python
from analytics_tracker import AnalyticsTracker

analytics = AnalyticsTracker(config)
await analytics.initialize()
```

#### Track Product Creation
```python
await analytics.track_product_creation(product_ids)
```

#### Track Sale
```python
await analytics.track_sale(
    product_id="prod_123",
    amount=4500,  # in cents
    customer_email="customer@example.com",
    platform="whop"
)
```

#### Generate Reports
```python
# Daily report
daily_report = await analytics.generate_daily_report()

# Weekly report
weekly_report = await analytics.generate_weekly_report()

# Revenue metrics
revenue_metrics = await analytics.get_revenue_metrics()

# Niche performance
niche_performance = await analytics.get_niche_performance()

# Revenue prediction
prediction = await analytics.predict_revenue(days_ahead=30)
```

### ContentCreator

#### Initialize
```python
from content_creator import ContentCreator

content_creator = ContentCreator(config)
await content_creator.initialize()
```

#### Create Campaign Content
```python
campaign_content = await content_creator.create_campaign_content(prompts)
# Returns Dict with social_media_posts, email_sequences, blog_content, ad_copy
```

#### Generate Social Posts
```python
social_posts = await content_creator.generate_social_posts(prompt)
# Returns List[Dict] with platform-specific posts
```

### CustomerManager

#### Initialize
```python
from customer_manager import CustomerManager

customer_manager = CustomerManager(config)
await customer_manager.initialize()
```

#### Add Customer
```python
customer_id = await customer_manager.add_customer(
    email="customer@example.com",
    first_name="John",
    last_name="Doe"
)
```

#### Record Purchase
```python
await customer_manager.record_purchase(
    customer_email="customer@example.com",
    product_id="prod_123",
    amount=4500  # in cents
)
```

#### Get Customer Analytics
```python
customer_analytics = await customer_manager.get_customer_analytics()
```

#### Send Marketing Campaign
```python
recipients_count = await customer_manager.send_marketing_campaign(
    campaign_name="Summer Sale 2025",
    subject="🔥 50% Off All AI Prompts!",
    content="Limited time offer...",
    target_segment="vip"  # "all", "new", "regular", "vip"
)
```

---

## 🔧 Configuration API

### Config Class

```python
from config import Config

config = Config()

# Access settings
print(config.DAILY_PROMPT_GENERATION)  # 50
print(config.PROFITABLE_NICHES)  # List of niches
print(config.AI_MODELS)  # Dict of AI models

# Get niche keywords
keywords = config.get_niche_keywords("Business & Marketing")

# Get dynamic pricing
price = config.get_pricing_strategy(
    niche="Business & Marketing",
    quality_score=0.87
)
```

### Environment Variables

```python
import os

# Required
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHOP_API_KEY = os.getenv("WHOP_API_KEY")

# Optional
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
```

---

## 📋 Data Models

### Prompt Object
```python
{
    "id": "prompt_12345",
    "title": "Advanced Marketing Strategy Framework",
    "prompt": "Act as an expert marketing strategist...",
    "description": "Professional marketing prompt for...",
    "niche": "Business & Marketing",
    "keywords": ["marketing", "strategy", "campaigns"],
    "template_type": "Strategic Analysis",
    "quality_score": 0.87,
    "created_at": "2025-08-04T12:00:00Z",
    "whop_product_id": "whop_prod_abc123"
}
```

### Sale Object
```python
{
    "id": 1,
    "product_id": "prompt_12345",
    "amount": 4500,  # in cents
    "customer_email": "customer@example.com",
    "sale_date": "2025-08-04T12:00:00Z",
    "platform": "whop"
}
```

### Customer Object
```python
{
    "id": 1,
    "email": "customer@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "registration_date": "2025-08-04T12:00:00Z",
    "total_purchases": 3,
    "total_spent": 135.00,
    "status": "active",
    "last_activity": "2025-08-04T12:00:00Z"
}
```

---

## 🚨 Error Handling

### Common Error Responses

```json
{
    "error": "Analytics unavailable",
    "code": 500,
    "timestamp": "2025-08-04T12:00:00Z"
}
```

### Exception Classes

```python
class NosytAPIError(Exception):
    """Base exception for Nosyt API errors"""
    pass

class GenerationError(NosytAPIError):
    """Prompt generation failed"""
    pass

class WhopIntegrationError(NosytAPIError):
    """WHOP API integration failed"""
    pass

class AnalyticsError(NosytAPIError):
    """Analytics system error"""
    pass
```

### Error Handling Example

```python
try:
    prompts = await generator.generate_daily_batch()
except GenerationError as e:
    logger.error(f"Generation failed: {str(e)}")
    # Fallback to template generation
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    # Send alert notification
```

---

## 🔐 Authentication

### API Key Authentication
```python
headers = {
    "Authorization": f"Bearer {WHOP_API_KEY}",
    "Content-Type": "application/json"
}
```

### Rate Limiting
- **OpenAI API**: 60 requests/minute
- **WHOP API**: 100 requests/minute
- **Internal APIs**: No limits

---

## 📈 Performance Optimization

### Async Operations
```python
# Parallel processing
tasks = [
    generator.generate_niche_prompts(niche, 5)
    for niche in config.PROFITABLE_NICHES
]
all_prompts = await asyncio.gather(*tasks)
```

### Caching
```python
# Cache expensive operations
@lru_cache(maxsize=100)
def get_niche_keywords(niche: str):
    return expensive_keyword_lookup(niche)
```

### Database Optimization
```python
# Batch operations
cursor.executemany(
    "INSERT INTO products (id, title, niche) VALUES (?, ?, ?)",
    [(p['id'], p['title'], p['niche']) for p in prompts]
)
```

---

## 🧪 Testing

### Unit Tests
```python
import pytest
from prompt_generator import PromptGenerator

@pytest.mark.asyncio
async def test_prompt_generation():
    generator = PromptGenerator(mock_config)
    prompts = await generator.generate_niche_prompts("Business", 1)
    assert len(prompts) == 1
    assert prompts[0]['quality_score'] >= 0.8
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_full_automation_cycle():
    system = NosytAutomationSystem()
    await system.initialize()
    await system.run_daily_automation()
    # Verify products created, analytics updated
```

---

**Need help with the API?**
- 📧 Email: api-support@nosyt.com
- 💬 Discord: [Join our developer community]
- 📖 More docs: `/docs/`

---

*Built with ❤️ by Nosyt LLC - Professional AI Automation*