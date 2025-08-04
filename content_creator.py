#!/usr/bin/env python3
"""
Content Creation Engine for Marketing Materials
"""

import openai
import asyncio
from typing import List, Dict
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ContentCreator:
    """AI-powered marketing content creation"""
    
    def __init__(self, config):
        self.config = config
        self.openai_client = None
        
    async def initialize(self):
        """Initialize content creation system"""
        if self.config.OPENAI_API_KEY:
            self.openai_client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            logger.info("✅ Content Creator initialized")
        else:
            logger.warning("⚠️ OpenAI API key not found - using templates")
    
    async def create_campaign_content(self, prompts: List[Dict]) -> Dict:
        """Create comprehensive marketing campaign content"""
        logger.info(f"📝 Creating marketing content for {len(prompts)} products...")
        
        campaign_content = {
            "social_media_posts": await self.create_social_media_content(prompts),
            "email_sequences": await self.create_email_marketing(prompts),
            "blog_content": await self.create_blog_content(prompts),
            "ad_copy": await self.create_ad_copy(prompts),
            "press_releases": await self.create_press_releases(prompts)
        }
        
        logger.info("✅ Marketing campaign content created")
        return campaign_content
    
    async def create_social_media_content(self, prompts: List[Dict]) -> List[Dict]:
        """Generate social media posts for products"""
        social_posts = []
        
        for prompt in prompts[:5]:  # Limit to top 5 products
            posts = await self.generate_social_posts(prompt)
            social_posts.extend(posts)
        
        return social_posts
    
    async def generate_social_posts(self, prompt: Dict) -> List[Dict]:
        """Generate social media posts for a single product"""
        platforms = ['twitter', 'linkedin', 'facebook', 'instagram']
        posts = []
        
        for platform in platforms:
            try:
                post_content = await self.create_platform_post(prompt, platform)
                posts.append({
                    'platform': platform,
                    'content': post_content,
                    'hashtags': self.generate_hashtags(prompt, platform),
                    'product_title': prompt['title'],
                    'niche': prompt['niche']
                })
            except Exception as e:
                logger.error(f"❌ Failed to create {platform} post: {str(e)}")
                # Fallback to template
                posts.append(self.create_template_post(prompt, platform))
        
        return posts
    
    async def create_platform_post(self, prompt: Dict, platform: str) -> str:
        """Create platform-specific social media post"""
        
        platform_specs = {
            'twitter': {'max_chars': 280, 'style': 'concise and engaging'},
            'linkedin': {'max_chars': 1300, 'style': 'professional and informative'},
            'facebook': {'max_chars': 500, 'style': 'conversational and relatable'},
            'instagram': {'max_chars': 300, 'style': 'visual and inspiring'}
        }
        
        spec = platform_specs[platform]
        
        generation_prompt = f"""
        Create a {platform} post promoting an AI prompt product.
        
        Product: {prompt['title']}
        Niche: {prompt['niche']}
        Keywords: {', '.join(prompt['keywords'])}
        
        Requirements:
        - Max {spec['max_chars']} characters
        - {spec['style']} tone
        - Include call-to-action
        - Highlight benefits and value
        - Make it shareable and engaging
        
        Generate only the post content.
        """
        
        if self.openai_client:
            try:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are an expert social media marketer creating {platform} content."},
                        {"role": "user", "content": generation_prompt}
                    ],
                    max_tokens=200,
                    temperature=0.8
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"❌ OpenAI failed for {platform} post: {str(e)}")
        
        # Fallback template
        return self.create_template_post(prompt, platform)['content']
    
    def create_template_post(self, prompt: Dict, platform: str) -> Dict:
        """Create template-based social media post"""
        templates = {
            'twitter': f"🤖 New AI prompt for {prompt['niche']}! \n\n{prompt['title']} \n\nGet instant professional results with this proven prompt template. \n\n💡 Perfect for: {prompt['keywords'][0]} \n⚡ Instant download \n\n#AI #Prompts #{prompt['niche'].replace(' ', '')} #Productivity",
            
            'linkedin': f"🚀 Boost Your {prompt['niche']} Results with AI \n\nIntroducing: {prompt['title']} \n\nThis professional AI prompt helps you: \n✅ Save hours of work \n✅ Get consistent results \n✅ Improve quality output \n\nPerfect for professionals working with {', '.join(prompt['keywords'][:3])} \n\nReady to 10x your productivity? Get instant access now! \n\n#ArtificialIntelligence #Productivity #Business #Automation",
            
            'facebook': f"🔥 Game-changing AI prompt for {prompt['niche']} professionals! \n\n{prompt['title']} \n\nStop struggling with {prompt['keywords'][0]} - this AI prompt does the heavy lifting for you! \n\n✨ Professional results in minutes \n💰 Save time and money \n🎯 Proven to work \n\nWho else needs this? Tag someone who works in {prompt['niche']}! 👇",
            
            'instagram': f"✨ {prompt['title']} \n\n🤖 AI-powered {prompt['niche']} solution \n💡 Professional results instantly \n⚡ Download & use today \n\n#AIPrompts #Productivity #Business #Automation #{prompt['niche'].replace(' ', '')}"
        }
        
        return {
            'platform': platform,
            'content': templates.get(platform, templates['twitter']),
            'hashtags': self.generate_hashtags(prompt, platform),
            'product_title': prompt['title'],
            'niche': prompt['niche']
        }
    
    def generate_hashtags(self, prompt: Dict, platform: str) -> List[str]:
        """Generate relevant hashtags for social media"""
        base_hashtags = ['AI', 'Prompts', 'Automation', 'Productivity', 'Business']
        
        niche_hashtags = {
            'Business & Marketing': ['Marketing', 'Business', 'Strategy', 'Growth'],
            'Content Creation & Copywriting': ['Content', 'Copywriting', 'Writing', 'CreativeWriting'],
            'E-commerce & Sales': ['Ecommerce', 'Sales', 'OnlineBusiness', 'Shopify'],
            'Programming & Development': ['Coding', 'Programming', 'Development', 'Tech'],
            'Personal Productivity': ['Productivity', 'TimeManagement', 'Goals', 'Success']
        }
        
        hashtags = base_hashtags + niche_hashtags.get(prompt['niche'], [])
        
        # Add keyword-based hashtags
        for keyword in prompt['keywords'][:2]:
            hashtag = keyword.replace(' ', '').replace('-', '').title()
            hashtags.append(hashtag)
        
        # Platform-specific hashtag limits
        limits = {'twitter': 10, 'linkedin': 15, 'facebook': 8, 'instagram': 20}
        limit = limits.get(platform, 10)
        
        return hashtags[:limit]
    
    async def create_email_marketing(self, prompts: List[Dict]) -> List[Dict]:
        """Create email marketing sequences"""
        email_sequences = []
        
        # Welcome sequence
        welcome_sequence = await self.create_welcome_sequence()
        email_sequences.append(welcome_sequence)
        
        # Product launch emails
        for prompt in prompts[:3]:  # Top 3 products
            launch_email = await self.create_product_launch_email(prompt)
            email_sequences.append(launch_email)
        
        # Weekly newsletter
        newsletter = await self.create_newsletter(prompts)
        email_sequences.append(newsletter)
        
        return email_sequences
    
    async def create_welcome_sequence(self) -> Dict:
        """Create welcome email sequence"""
        return {
            'type': 'welcome_sequence',
            'subject': '🎉 Welcome to Nosyt AI - Your Prompt Empire Starts Here!',
            'content': f"""
Hi there! 👋

Welcome to Nosyt AI - where we turn artificial intelligence into your personal profit machine!

I'm excited you've joined our community of smart entrepreneurs who are using AI prompts to:

✨ Save 10+ hours per week
💰 Generate consistent income
🚀 Scale their businesses faster
📈 Get professional results instantly

As a new member, here's what you get:

🎁 FREE Starter Pack: 10 High-Converting AI Prompts
📚 AI Profit Blueprint (usually $97)
💬 Access to our exclusive Discord community
⚡ Daily profit tips and strategies

Ready to start your AI-powered business?

[DOWNLOAD YOUR FREE STARTER PACK]

To your success,
Tyson @ Nosyt LLC
New Mexico

P.S. Keep an eye on your inbox - I'll be sharing my best AI profit secrets with you this week!
""",
            'call_to_action': 'Download Free Starter Pack',
            'sequence_day': 1
        }
    
    async def create_product_launch_email(self, prompt: Dict) -> Dict:
        """Create product launch email"""
        return {
            'type': 'product_launch',
            'subject': f"🔥 NEW: {prompt['title']} (Limited Time)",
            'content': f"""
BIG NEWS! 🎉

I just released something incredible for {prompt['niche']} professionals...

📦 **{prompt['title']}**

This AI prompt is already getting amazing results:

✅ Professional output in under 5 minutes
✅ No more writer's block or creative struggles  
✅ Proven template that works every time
✅ Perfect for: {', '.join(prompt['keywords'][:3])}

🏆 **What makes this special?**

• Quality Score: {prompt['quality_score']:.1f}/1.0 (Top Tier)
• Template Type: {prompt['template_type']}
• Instant download & lifetime access
• 30-day money-back guarantee

💰 **Special Launch Price: Just ${self.config.get_pricing_strategy(prompt['niche'], prompt['quality_score'])}**

(Regular price will be ${self.config.get_pricing_strategy(prompt['niche'], prompt['quality_score']) + 20} after this week)

[GET IT NOW - LIMITED TIME]

Don't miss out - this price won't last!

Tyson @ Nosyt LLC

P.S. Only 48 hours left at this special price!
""",
            'call_to_action': 'Get Limited Time Access',
            'product_id': prompt.get('id', 'unknown')
        }
    
    async def create_newsletter(self, prompts: List[Dict]) -> Dict:
        """Create weekly newsletter"""
        top_niches = list(set([p['niche'] for p in prompts[:5]]))
        
        return {
            'type': 'newsletter',
            'subject': '📊 This Week in AI Profits + New Releases',
            'content': f"""
🤖 **Nosyt AI Weekly Report**

Hey Profit Makers!

Here's what's happening in the AI prompt world:

📈 **This Week's Numbers:**
• {len(prompts)} new prompts created
• Top performing niches: {', '.join(top_niches[:3])}
• Average quality score: {sum(p['quality_score'] for p in prompts)/len(prompts):.2f}/1.0

🔥 **Trending Niches:**
{chr(10).join([f'• {niche}' for niche in top_niches[:5]])}

💡 **AI Profit Tip of the Week:**
Combine multiple prompts from different niches to create unique solutions. For example, mix "Business Strategy" + "Content Creation" prompts for comprehensive marketing campaigns.

🆕 **New This Week:**
{chr(10).join([f'• {p["title"]}' for p in prompts[:3]])}

💰 **Member Spotlight:**
"I made $847 this week using Nosyt prompts for my consulting business!" - Sarah M., Business Coach

[BROWSE ALL NEW PROMPTS]

Keep crushing it!
Tyson @ Nosyt LLC

P.S. Got a prompt request? Just reply to this email!
""",
            'call_to_action': 'Browse New Prompts'
        }
    
    async def create_blog_content(self, prompts: List[Dict]) -> List[Dict]:
        """Create blog content for SEO and authority building"""
        blog_posts = []
        
        # How-to guides
        for niche in list(set([p['niche'] for p in prompts]))[:3]:
            blog_post = await self.create_how_to_guide(niche, prompts)
            blog_posts.append(blog_post)
        
        # Industry trends post
        trends_post = await self.create_trends_post(prompts)
        blog_posts.append(trends_post)
        
        return blog_posts
    
    async def create_how_to_guide(self, niche: str, prompts: List[Dict]) -> Dict:
        """Create how-to guide for specific niche"""
        niche_prompts = [p for p in prompts if p['niche'] == niche]
        
        return {
            'type': 'how_to_guide',
            'title': f'How to Use AI Prompts for {niche}: Complete 2025 Guide',
            'content': f"""
# How to Use AI Prompts for {niche}: Complete 2025 Guide

AI prompts are revolutionizing {niche.lower()} by automating complex tasks and delivering professional results in minutes.

## What Are AI Prompts?

AI prompts are carefully crafted instructions that guide artificial intelligence to produce specific, high-quality outputs for your {niche.lower()} needs.

## Top {niche} Use Cases:

{chr(10).join([f'• {p["keywords"][0].title()}' for p in niche_prompts[:5]])}

## Step-by-Step Implementation:

### 1. Choose the Right Prompt
Select prompts based on your specific {niche.lower()} goals and current challenges.

### 2. Customize for Your Needs
Replace placeholders with your specific information and requirements.

### 3. Execute and Refine
Run the prompt and adjust based on your results.

## Best Practices:

✅ Be specific with your inputs
✅ Test different variations
✅ Save successful prompt combinations
✅ Track your results and improvements

## Recommended Prompts for {niche}:

{chr(10).join([f'• **{p["title"]}** - {p["description"][:100]}...' for p in niche_prompts[:3]])}

## Conclusion

AI prompts can transform your {niche.lower()} workflow, saving time while improving quality. Start with proven templates and customize them for your specific needs.

[GET STARTED WITH {niche.upper()} PROMPTS]
""",
            'meta_description': f'Learn how to use AI prompts for {niche.lower()}. Complete guide with examples, best practices, and proven templates for 2025.',
            'keywords': [niche.lower().replace(' ', '-'), 'ai-prompts', 'automation', 'productivity'],
            'call_to_action': f'Get {niche} Prompts'
        }
    
    async def create_trends_post(self, prompts: List[Dict]) -> Dict:
        """Create AI trends blog post"""
        top_niches = list(set([p['niche'] for p in prompts]))
        
        return {
            'type': 'trends',
            'title': 'AI Prompt Trends 2025: What\'s Working Now',
            'content': f"""
# AI Prompt Trends 2025: What's Working Now

The AI prompt marketplace is exploding, and smart entrepreneurs are cashing in. Here's what's trending right now.

## Top Performing Niches:

{chr(10).join([f'### {i+1}. {niche}' + chr(10) + f'High demand for automation in {niche.lower()} continues to drive sales.' for i, niche in enumerate(top_niches[:5])])}

## Quality Standards Rising

Our data shows prompts with quality scores above 0.8 are selling 3x better than average.

**Average Quality Score This Month:** {sum(p['quality_score'] for p in prompts)/len(prompts):.2f}/1.0

## Template Types That Convert:

• Strategic Analysis Prompts
• Step-by-Step Frameworks
• Creative Problem-Solving Templates
• Data-Driven Decision Tools

## Market Predictions:

🔮 **What's Coming:**
• Multi-modal prompts (text + image)
• Industry-specific AI assistants
• Automated prompt optimization
• Real-time performance tracking

## Action Steps:

1. Focus on high-demand niches
2. Prioritize quality over quantity
3. Create comprehensive prompt packages
4. Build recurring revenue streams

[EXPLORE TRENDING PROMPTS]
""",
            'meta_description': 'Discover the hottest AI prompt trends for 2025. Market insights, performance data, and predictions for smart entrepreneurs.',
            'keywords': ['ai-prompt-trends', 'digital-products-2025', 'ai-automation', 'online-business'],
            'call_to_action': 'Explore Trending Prompts'
        }
    
    async def create_ad_copy(self, prompts: List[Dict]) -> List[Dict]:
        """Create paid advertising copy"""
        ad_campaigns = []
        
        # Google Ads
        google_ads = await self.create_google_ads(prompts[:3])
        ad_campaigns.extend(google_ads)
        
        # Facebook Ads  
        facebook_ads = await self.create_facebook_ads(prompts[:3])
        ad_campaigns.extend(facebook_ads)
        
        return ad_campaigns
    
    async def create_google_ads(self, prompts: List[Dict]) -> List[Dict]:
        """Create Google Ads copy"""
        ads = []
        
        for prompt in prompts:
            ad = {
                'platform': 'google_ads',
                'product_title': prompt['title'],
                'headlines': [
                    f"{prompt['title']}",
                    f"Professional {prompt['niche']} AI Prompt",
                    f"Get Results in Minutes with AI",
                    f"${self.config.get_pricing_strategy(prompt['niche'], prompt['quality_score'])} - Instant Download"
                ],
                'descriptions': [
                    f"Professional AI prompt for {prompt['niche']}. Quality score {prompt['quality_score']:.1f}/1.0. Instant download.",
                    f"Save hours of work with this proven {prompt['template_type'].lower()} template. Get professional results fast."
                ],
                'keywords': prompt['keywords'] + ['ai prompts', 'automation', prompt['niche'].lower()],
                'call_to_action': 'Download Now'
            }
            ads.append(ad)
        
        return ads
    
    async def create_facebook_ads(self, prompts: List[Dict]) -> List[Dict]:
        """Create Facebook Ads copy"""
        ads = []
        
        for prompt in prompts:
            ad = {
                'platform': 'facebook_ads',
                'product_title': prompt['title'],
                'primary_text': f"🤖 Stop struggling with {prompt['keywords'][0]}! This AI prompt delivers professional {prompt['niche'].lower()} results in minutes. Quality score: {prompt['quality_score']:.1f}/1.0 ⭐",
                'headline': f"{prompt['title']}",
                'description': f"Professional AI prompt - ${self.config.get_pricing_strategy(prompt['niche'], prompt['quality_score'])} - Instant download",
                'call_to_action': 'Learn More',
                'target_interests': prompt['keywords'] + ['artificial intelligence', 'business automation', 'productivity tools']
            }
            ads.append(ad)
        
        return ads
    
    async def create_press_releases(self, prompts: List[Dict]) -> List[Dict]:
        """Create press releases for major product launches"""
        if len(prompts) < 10:  # Only create PR for significant launches
            return []
        
        press_release = {
            'type': 'press_release',
            'title': f'Nosyt LLC Launches Revolutionary AI Prompt Collection for {len(set([p["niche"] for p in prompts]))} Industries',
            'content': f"""
FOR IMMEDIATE RELEASE

Nosyt LLC Launches Revolutionary AI Prompt Collection for {len(set([p["niche"] for p in prompts]))} Industries

New Mexico-based company releases {len(prompts)} professional AI prompts to help businesses automate complex tasks

MONCTON, NB / NEW MEXICO - {datetime.now().strftime('%B %d, %Y')} - Nosyt LLC, a leading provider of AI automation solutions, today announced the launch of its comprehensive AI prompt collection, featuring {len(prompts)} professionally crafted prompts across {len(set([p["niche"] for p in prompts]))} key industries.

The new collection addresses the growing demand for AI-powered business automation, offering ready-to-use prompts that deliver professional results in minutes rather than hours.

"We're seeing unprecedented demand for AI automation tools," said Tyson, Founder of Nosyt LLC. "Our prompts have helped thousands of professionals save 10+ hours per week while improving their output quality."

Key features of the new collection include:

• Average quality score of {sum(p['quality_score'] for p in prompts)/len(prompts):.2f}/1.0
• Coverage of high-demand niches including {', '.join(list(set([p['niche'] for p in prompts]))[:3])}
• Instant download and lifetime access
• Professional templates and frameworks

The prompts are available immediately through the WHOP marketplace, with pricing starting at $15.

About Nosyt LLC:
Based in New Mexico and operated from Moncton, NB, Canada, Nosyt LLC specializes in AI automation solutions for businesses and entrepreneurs. The company is committed to making artificial intelligence accessible and profitable for professionals across all industries.

For more information, visit [website] or contact [email].

###
"""
        }
        
        return [press_release]