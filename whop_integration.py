#!/usr/bin/env python3
"""
WHOP Marketplace Integration for Nosyt AI Prompt Automation
"""

import aiohttp
import asyncio
import json
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class WhopIntegration:
    """WHOP marketplace API integration"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = "https://api.whop.com/v1"
        self.session = None
        self.headers = {
            "Authorization": f"Bearer {config.WHOP_API_KEY}",
            "Content-Type": "application/json"
        }
    
    async def initialize(self):
        """Initialize WHOP API connection"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        
        # Test API connection
        try:
            await self.test_connection()
            logger.info("✅ WHOP API connection established")
        except Exception as e:
            logger.error(f"❌ WHOP API connection failed: {str(e)}")
            # Use mock mode for development
            self.mock_mode = True
            logger.info("🔧 Running in mock mode for development")
    
    async def test_connection(self):
        """Test WHOP API connection"""
        async with self.session.get(f"{self.base_url}/me") as response:
            if response.status == 200:
                data = await response.json()
                logger.info(f"🔗 Connected to WHOP as: {data.get('username', 'Unknown')}")
            else:
                raise Exception(f"API test failed with status {response.status}")
    
    async def create_products(self, prompts: List[Dict], marketing_content: Dict) -> List[str]:
        """Create products on WHOP marketplace"""
        logger.info(f"🛒 Creating {len(prompts)} products on WHOP...")
        
        product_ids = []
        
        for prompt in prompts:
            try:
                product_id = await self.create_single_product(prompt, marketing_content)
                if product_id:
                    product_ids.append(product_id)
                    logger.info(f"✅ Created product: {prompt['title']} (ID: {product_id})")
                
                # Rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Failed to create product {prompt['title']}: {str(e)}")
                continue
        
        logger.info(f"🎉 Successfully created {len(product_ids)} products on WHOP")
        return product_ids
    
    async def create_single_product(self, prompt: Dict, marketing_content: Dict) -> Optional[str]:
        """Create single product on WHOP"""
        
        # Calculate price based on niche and quality
        price = self.config.get_pricing_strategy(prompt['niche'], prompt['quality_score'])
        
        # Prepare product data
        product_data = {
            "name": prompt['title'],
            "description": self.format_product_description(prompt, marketing_content),
            "price": price * 100,  # Price in cents
            "type": "digital_product",
            "category": self.map_niche_to_category(prompt['niche']),
            "tags": prompt['keywords'] + ["AI", "Prompts", "Automation"],
            "files": await self.prepare_product_files(prompt),
            "instant_delivery": True,
            "unlimited_stock": True
        }
        
        if hasattr(self, 'mock_mode') and self.mock_mode:
            # Mock mode for development
            product_id = f"mock_{datetime.now().timestamp()}"
            logger.info(f"🔧 Mock product created: {product_id}")
            return product_id
        
        try:
            async with self.session.post(f"{self.base_url}/products", json=product_data) as response:
                if response.status == 201:
                    result = await response.json()
                    return result.get('id')
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Product creation failed: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ API request failed: {str(e)}")
            return None
    
    def format_product_description(self, prompt: Dict, marketing_content: Dict) -> str:
        """Format product description for WHOP"""
        
        description = f"""🤖 **Professional AI Prompt for {prompt['niche']}**

{prompt['description']}

**🎯 What You Get:**
• High-quality AI prompt (150-300 words)
• Detailed instructions and examples
• Ready-to-use with ChatGPT, Claude, or any AI
• Professional results in minutes
• Keywords: {', '.join(prompt['keywords'])}

**💡 Perfect For:**
• {prompt['niche']} professionals
• Content creators and marketers
• Business owners and entrepreneurs
• Anyone wanting to save time with AI

**⚡ Instant Delivery:**
Download immediately after purchase - no waiting!

**🏆 Quality Guarantee:**
Quality Score: {prompt['quality_score']:.1f}/1.0
Created by Nosyt LLC - Professional AI Solutions

**🔥 Limited Time:** Get this proven prompt template now!

---
*Built by Nosyt LLC - Your AI Automation Experts*"""
        
        return description
    
    def map_niche_to_category(self, niche: str) -> str:
        """Map niche to WHOP category"""
        category_mapping = {
            "Business & Marketing": "business",
            "Content Creation & Copywriting": "content",
            "E-commerce & Sales": "ecommerce",
            "Programming & Development": "development",
            "Personal Productivity": "productivity",
            "Social Media Marketing": "marketing",
            "Email Marketing": "marketing",
            "SEO & Digital Marketing": "marketing"
        }
        return category_mapping.get(niche, "tools")
    
    async def prepare_product_files(self, prompt: Dict) -> List[Dict]:
        """Prepare downloadable files for the product"""
        
        # Create formatted prompt file
        prompt_content = f"""# {prompt['title']}

## AI Prompt:

{prompt['prompt']}

## Usage Instructions:

1. Copy the prompt above
2. Paste it into ChatGPT, Claude, or your preferred AI
3. Replace any [PLACEHOLDER] text with your specific details
4. Run the prompt and get professional results!

## Keywords:
{', '.join(prompt['keywords'])}

## Template Type:
{prompt['template_type']}

## Created:
{prompt['created_at']}

---
Created by Nosyt LLC
Professional AI Solutions
"""
        
        # In a real implementation, you'd upload this to your file storage
        # For now, we'll return the file structure
        return [
            {
                "name": f"{prompt['title'].replace(' ', '_')}.txt",
                "content": prompt_content,
                "type": "text/plain"
            }
        ]
    
    async def update_product_analytics(self, product_ids: List[str]):
        """Update product performance analytics"""
        for product_id in product_ids:
            try:
                # Get product stats
                stats = await self.get_product_stats(product_id)
                # Update internal analytics
                await self.store_product_analytics(product_id, stats)
            except Exception as e:
                logger.error(f"❌ Failed to update analytics for {product_id}: {str(e)}")
    
    async def get_product_stats(self, product_id: str) -> Dict:
        """Get product performance statistics"""
        if hasattr(self, 'mock_mode') and self.mock_mode:
            # Return mock data
            return {
                "views": 45,
                "sales": 3,
                "revenue": 135,
                "conversion_rate": 0.067
            }
        
        try:
            async with self.session.get(f"{self.base_url}/products/{product_id}/stats") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {}
        except Exception as e:
            logger.error(f"❌ Failed to get stats for {product_id}: {str(e)}")
            return {}
    
    async def store_product_analytics(self, product_id: str, stats: Dict):
        """Store analytics data locally"""
        # Implementation would store in database
        logger.info(f"📊 Analytics for {product_id}: {stats}")
    
    async def close(self):
        """Close API session"""
        if self.session:
            await self.session.close()