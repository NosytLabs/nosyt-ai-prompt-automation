#!/usr/bin/env python3
"""
Nosyt AI Prompt Automation System
Main execution file for automated AI prompt generation and WHOP integration

Author: Nosyt LLC
Date: 2025-08-04
"""

import asyncio
import logging
from datetime import datetime
from config import Config
from prompt_generator import PromptGenerator
from whop_integration import WhopIntegration
from content_creator import ContentCreator
from automation_scheduler import AutomationScheduler
from analytics_tracker import AnalyticsTracker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nosyt_automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class NosytAutomationSystem:
    """Main automation system orchestrator"""
    
    def __init__(self):
        self.config = Config()
        self.prompt_generator = PromptGenerator(self.config)
        self.whop_integration = WhopIntegration(self.config)
        self.content_creator = ContentCreator(self.config)
        self.scheduler = AutomationScheduler(self.config)
        self.analytics = AnalyticsTracker(self.config)
        
    async def initialize(self):
        """Initialize all system components"""
        logger.info("🚀 Initializing Nosyt AI Prompt Automation System...")
        
        # Initialize components
        await self.prompt_generator.initialize()
        await self.whop_integration.initialize()
        await self.content_creator.initialize()
        await self.analytics.initialize()
        
        logger.info("✅ System initialization complete!")
    
    async def run_daily_automation(self):
        """Run daily automated tasks"""
        logger.info("🔄 Starting daily automation cycle...")
        
        try:
            # Generate new prompts
            logger.info("📝 Generating new AI prompts...")
            new_prompts = await self.prompt_generator.generate_daily_batch()
            
            # Create marketing content
            logger.info("📢 Creating marketing materials...")
            marketing_content = await self.content_creator.create_campaign_content(new_prompts)
            
            # Upload to WHOP
            logger.info("🛒 Uploading products to WHOP marketplace...")
            product_ids = await self.whop_integration.create_products(new_prompts, marketing_content)
            
            # Track analytics
            logger.info("📊 Updating analytics...")
            await self.analytics.track_product_creation(product_ids)
            
            # Generate performance report
            report = await self.analytics.generate_daily_report()
            logger.info(f"📈 Daily Report: {report}")
            
            logger.info("✅ Daily automation cycle completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error in daily automation: {str(e)}")
            # Send alert notification
            await self.send_error_alert(str(e))
    
    async def send_error_alert(self, error_message):
        """Send error notifications"""
        # Implementation for error alerts (email, Discord, etc.)
        pass
    
    async def start_automation(self):
        """Start the main automation loop"""
        logger.info("🎯 Starting Nosyt AI Prompt Automation System...")
        
        # Schedule daily tasks
        self.scheduler.schedule_daily_automation(self.run_daily_automation)
        
        # Start web interface
        from web_interface import create_app
        app = create_app(self)
        
        logger.info("🌐 Web interface available at: http://localhost:8000")
        logger.info("💰 Revenue tracking dashboard: http://localhost:8000/dashboard")
        
        # Keep running
        while True:
            await self.scheduler.run_pending()
            await asyncio.sleep(60)  # Check every minute

async def main():
    """Main entry point"""
    print("""
    🤖 NOSYT AI PROMPT AUTOMATION SYSTEM 🤖
    =========================================
    
    💡 Automated AI Prompt Generation & Sales
    🛒 WHOP Marketplace Integration
    💰 Passive Income Generation
    📊 Analytics & Performance Tracking
    
    Built for Nosyt LLC - New Mexico
    =========================================
    """)
    
    system = NosytAutomationSystem()
    
    try:
        await system.initialize()
        await system.start_automation()
    except KeyboardInterrupt:
        logger.info("🛑 System shutdown requested...")
    except Exception as e:
        logger.error(f"💥 Critical system error: {str(e)}")
    finally:
        logger.info("👋 Nosyt Automation System stopped.")

if __name__ == "__main__":
    asyncio.run(main())