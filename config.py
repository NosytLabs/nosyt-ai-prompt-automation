#!/usr/bin/env python3
"""
Configuration settings for Nosyt AI Prompt Automation System
"""

import os
from typing import Dict, List
from pydantic import BaseSettings

class Config(BaseSettings):
    """System configuration"""
    
    # API Keys (Set these in your environment)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    WHOP_API_KEY: str = os.getenv("WHOP_API_KEY", "")
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY", "")
    
    # Business Settings
    COMPANY_NAME: str = "Nosyt LLC"
    COMPANY_LOCATION: str = "New Mexico"
    OWNER_LOCATION: str = "Moncton, NB, Canada"
    
    # Product Settings
    DAILY_PROMPT_GENERATION: int = 50
    PROMPT_PACK_SIZE: int = 25
    BASE_PRICE_RANGE: tuple = (15, 50)
    PREMIUM_PRICE_RANGE: tuple = (97, 297)
    
    # Profitable Niches (Based on market research)
    PROFITABLE_NICHES: List[str] = [
        "Business & Marketing",
        "Content Creation & Copywriting", 
        "E-commerce & Sales",
        "Programming & Development",
        "Personal Productivity",
        "Social Media Marketing",
        "Email Marketing",
        "SEO & Digital Marketing",
        "Creative Writing",
        "Educational Content",
        "Health & Fitness",
        "Real Estate",
        "Finance & Investment",
        "Customer Service",
        "Data Analysis"
    ]
    
    # AI Model Settings
    AI_MODELS: Dict[str, str] = {
        "primary": "gpt-4",
        "secondary": "claude-3-sonnet",
        "fallback": "gpt-3.5-turbo"
    }
    
    # WHOP Integration Settings
    WHOP_BASE_URL: str = "https://api.whop.com/v1"
    AUTO_PUBLISH: bool = True
    AUTO_PRICING: bool = True
    
    # Automation Schedule
    GENERATION_SCHEDULE: str = "09:00"  # 9 AM daily
    ANALYTICS_SCHEDULE: str = "18:00"   # 6 PM daily
    MARKETING_SCHEDULE: str = "12:00"   # 12 PM daily
    
    # Revenue Targets
    MONTHLY_REVENUE_TARGET: int = 5000
    DAILY_PRODUCT_TARGET: int = 10
    
    # Quality Control
    MIN_PROMPT_QUALITY_SCORE: float = 0.8
    MAX_RETRIES: int = 3
    
    # File Paths
    DATA_DIR: str = "data"
    LOGS_DIR: str = "logs"
    TEMPLATES_DIR: str = "templates"
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///nosyt_automation.db")
    
    # Notification Settings
    DISCORD_WEBHOOK: str = os.getenv("DISCORD_WEBHOOK", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_niche_keywords(self, niche: str) -> List[str]:
        """Get relevant keywords for each niche"""
        niche_keywords = {
            "Business & Marketing": [
                "lead generation", "sales funnel", "customer acquisition",
                "brand strategy", "market research", "competitive analysis",
                "business plan", "ROI optimization", "conversion rate"
            ],
            "Content Creation & Copywriting": [
                "blog posts", "sales copy", "email sequences",
                "social media content", "ad copy", "headlines",
                "storytelling", "persuasive writing", "content strategy"
            ],
            "E-commerce & Sales": [
                "product descriptions", "Amazon listings", "sales pages",
                "checkout optimization", "upsell strategies", "cart abandonment",
                "customer reviews", "product photography", "inventory management"
            ],
            "Programming & Development": [
                "code generation", "debugging", "API documentation",
                "database design", "testing strategies", "deployment",
                "performance optimization", "security best practices", "architecture"
            ],
            "Personal Productivity": [
                "time management", "goal setting", "habit formation",
                "workflow optimization", "task prioritization", "focus techniques",
                "productivity systems", "motivation", "work-life balance"
            ]
        }
        
        return niche_keywords.get(niche, [])
    
    def get_pricing_strategy(self, niche: str, quality_score: float) -> int:
        """Dynamic pricing based on niche and quality"""
        base_prices = {
            "Business & Marketing": 35,
            "E-commerce & Sales": 45,
            "Programming & Development": 50,
            "Content Creation & Copywriting": 25,
            "Personal Productivity": 20
        }
        
        base_price = base_prices.get(niche, 30)
        quality_multiplier = 1 + (quality_score - 0.5)  # 0.5-1.5x multiplier
        
        return int(base_price * quality_multiplier)