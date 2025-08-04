#!/usr/bin/env python3
"""
AI Prompt Generation Engine for Nosyt Automation System
"""

import asyncio
import openai
import random
from typing import List, Dict, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PromptGenerator:
    """Advanced AI prompt generation system"""
    
    def __init__(self, config):
        self.config = config
        self.openai_client = None
        self.quality_scorer = PromptQualityScorer()
        
    async def initialize(self):
        """Initialize the prompt generator"""
        if self.config.OPENAI_API_KEY:
            openai.api_key = self.config.OPENAI_API_KEY
            self.openai_client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            logger.info("✅ OpenAI API initialized")
        else:
            logger.warning("⚠️ OpenAI API key not found")
    
    async def generate_daily_batch(self) -> List[Dict]:
        """Generate daily batch of AI prompts"""
        logger.info(f"🎯 Generating {self.config.DAILY_PROMPT_GENERATION} prompts...")
        
        all_prompts = []
        
        for niche in self.config.PROFITABLE_NICHES:
            niche_prompts = await self.generate_niche_prompts(niche, 3)
            all_prompts.extend(niche_prompts)
        
        # Sort by quality score
        all_prompts.sort(key=lambda x: x['quality_score'], reverse=True)
        
        # Return top prompts
        return all_prompts[:self.config.DAILY_PROMPT_GENERATION]
    
    async def generate_niche_prompts(self, niche: str, count: int) -> List[Dict]:
        """Generate prompts for specific niche"""
        logger.info(f"📝 Generating {count} prompts for {niche}...")
        
        prompts = []
        keywords = self.config.get_niche_keywords(niche)
        
        for i in range(count):
            try:
                # Generate primary prompt
                prompt_data = await self.create_single_prompt(niche, keywords)
                
                # Score quality
                quality_score = self.quality_scorer.score_prompt(prompt_data['prompt'])
                
                if quality_score >= self.config.MIN_PROMPT_QUALITY_SCORE:
                    prompt_data['quality_score'] = quality_score
                    prompt_data['niche'] = niche
                    prompt_data['created_at'] = datetime.now().isoformat()
                    prompts.append(prompt_data)
                    
            except Exception as e:
                logger.error(f"❌ Error generating prompt for {niche}: {str(e)}")
                continue
        
        return prompts
    
    async def create_single_prompt(self, niche: str, keywords: List[str]) -> Dict:
        """Create a single high-quality prompt"""
        
        # Select random keywords
        selected_keywords = random.sample(keywords, min(3, len(keywords)))
        
        # Prompt generation templates
        templates = self.get_prompt_templates(niche)
        template = random.choice(templates)
        
        # Generate using AI
        generation_prompt = f"""
        Create a highly effective AI prompt for {niche} professionals.
        
        Requirements:
        - Focus on: {', '.join(selected_keywords)}
        - Template style: {template}
        - Output should be practical and actionable
        - Include specific instructions and examples
        - Length: 150-300 words
        - Professional tone
        
        Generate only the prompt content, no explanations.
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.config.AI_MODELS['primary'],
                messages=[
                    {"role": "system", "content": "You are an expert prompt engineer creating valuable AI prompts for business professionals."},
                    {"role": "user", "content": generation_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            prompt_content = response.choices[0].message.content.strip()
            
            # Generate title and description
            title = await self.generate_prompt_title(prompt_content, niche)
            description = await self.generate_prompt_description(prompt_content, niche)
            
            return {
                'title': title,
                'prompt': prompt_content,
                'description': description,
                'keywords': selected_keywords,
                'template_type': template
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {str(e)}")
            # Fallback to template-based generation
            return self.generate_template_prompt(niche, selected_keywords, template)
    
    def get_prompt_templates(self, niche: str) -> List[str]:
        """Get prompt templates for each niche"""
        templates = {
            "Business & Marketing": [
                "Strategic Analysis", "Campaign Planning", "Market Research",
                "Competitive Intelligence", "Customer Journey Mapping", "ROI Optimization"
            ],
            "Content Creation & Copywriting": [
                "Persuasive Writing", "Storytelling Framework", "Content Strategy",
                "Audience Engagement", "Conversion Copywriting", "Brand Voice Development"
            ],
            "E-commerce & Sales": [
                "Product Optimization", "Sales Funnel Design", "Customer Retention",
                "Pricing Strategy", "Conversion Rate Optimization", "Customer Service Excellence"
            ],
            "Programming & Development": [
                "Code Architecture", "Problem Solving", "Performance Optimization",
                "Testing Strategy", "Documentation", "Debugging Process"
            ],
            "Personal Productivity": [
                "Goal Achievement", "Time Management", "Habit Formation",
                "Focus Enhancement", "Workflow Optimization", "Motivation Boost"
            ]
        }
        
        return templates.get(niche, ["General Framework", "Step-by-Step Guide", "Strategic Approach"])
    
    def generate_template_prompt(self, niche: str, keywords: List[str], template: str) -> Dict:
        """Generate prompt using templates (fallback method)"""
        
        base_prompts = {
            "Business & Marketing": f"""Act as an expert marketing strategist. Create a comprehensive {template.lower()} for {', '.join(keywords)}.
            
            Your response should include:
            1. Situation analysis
            2. Strategic recommendations
            3. Implementation steps
            4. Success metrics
            5. Risk mitigation strategies
            
            Provide specific, actionable insights that can be immediately implemented.""",
            
            "Content Creation & Copywriting": f"""You are a master copywriter. Develop {template.lower()} content focusing on {', '.join(keywords)}.
            
            Include:
            1. Target audience analysis
            2. Key messaging strategy
            3. Compelling headlines
            4. Persuasive body content
            5. Strong call-to-action
            
            Make it conversion-focused and emotionally engaging."""
        }
        
        prompt_content = base_prompts.get(niche, f"Create professional content about {', '.join(keywords)} using {template.lower()} approach.")
        
        return {
            'title': f"{template} for {niche}",
            'prompt': prompt_content,
            'description': f"Professional {template.lower()} prompt for {niche} focusing on {', '.join(keywords)}",
            'keywords': keywords,
            'template_type': template
        }
    
    async def generate_prompt_title(self, prompt_content: str, niche: str) -> str:
        """Generate catchy title for prompt"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Create catchy, sales-focused titles for AI prompts."},
                    {"role": "user", "content": f"Create a compelling title for this {niche} prompt: {prompt_content[:200]}..."}
                ],
                max_tokens=50,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except:
            return f"Professional {niche} AI Prompt"
    
    async def generate_prompt_description(self, prompt_content: str, niche: str) -> str:
        """Generate marketing description for prompt"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Write compelling product descriptions for AI prompts that highlight benefits and value."},
                    {"role": "user", "content": f"Write a sales description for this {niche} AI prompt: {prompt_content[:200]}..."}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except:
            return f"High-quality AI prompt for {niche} professionals. Get instant results and boost your productivity."

class PromptQualityScorer:
    """Quality scoring system for AI prompts"""
    
    def score_prompt(self, prompt: str) -> float:
        """Score prompt quality from 0.0 to 1.0"""
        score = 0.0
        
        # Length check (150-300 words optimal)
        word_count = len(prompt.split())
        if 150 <= word_count <= 300:
            score += 0.2
        elif 100 <= word_count <= 400:
            score += 0.1
        
        # Structure check (numbered lists, clear sections)
        if any(marker in prompt for marker in ['1.', '2.', '3.', '•', '-']):
            score += 0.2
        
        # Specificity check (specific terms, examples)
        specific_words = ['specific', 'example', 'include', 'detailed', 'step-by-step']
        if any(word in prompt.lower() for word in specific_words):
            score += 0.2
        
        # Professional language check
        professional_terms = ['professional', 'strategic', 'analysis', 'implementation', 'optimization']
        if any(term in prompt.lower() for term in professional_terms):
            score += 0.2
        
        # Actionable language check
        action_words = ['create', 'develop', 'analyze', 'implement', 'optimize', 'design']
        if any(word in prompt.lower() for word in action_words):
            score += 0.2
        
        return min(score, 1.0)