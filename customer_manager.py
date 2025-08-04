#!/usr/bin/env python3
"""
Customer Management and Support System
"""

import sqlite3
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import logging
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

logger = logging.getLogger(__name__)

class CustomerManager:
    """Comprehensive customer management system"""
    
    def __init__(self, config):
        self.config = config
        self.db_path = "nosyt_customers.db"
        self.conn = None
        
    async def initialize(self):
        """Initialize customer management system"""
        self.conn = sqlite3.connect(self.db_path)
        await self.create_tables()
        logger.info("✅ Customer management system initialized")
    
    async def create_tables(self):
        """Create customer database tables"""
        cursor = self.conn.cursor()
        
        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                first_name TEXT,
                last_name TEXT,
                registration_date TIMESTAMP,
                total_purchases INTEGER DEFAULT 0,
                total_spent INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                preferred_niches TEXT,
                last_activity TIMESTAMP
            )
        """)
        
        # Customer purchases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                product_id TEXT,
                purchase_date TIMESTAMP,
                amount INTEGER,
                status TEXT DEFAULT 'completed',
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)
        
        # Support tickets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS support_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                subject TEXT,
                message TEXT,
                status TEXT DEFAULT 'open',
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP,
                resolved_at TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)
        
        # Email campaigns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_name TEXT,
                subject TEXT,
                content TEXT,
                sent_at TIMESTAMP,
                recipients_count INTEGER,
                open_rate REAL,
                click_rate REAL
            )
        """)
        
        self.conn.commit()
        logger.info("📁 Customer database tables created")
    
    async def add_customer(self, email: str, first_name: str = "", last_name: str = "") -> int:
        """Add new customer to database"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO customers (email, first_name, last_name, registration_date, last_activity)
                VALUES (?, ?, ?, ?, ?)
            """, (email, first_name, last_name, datetime.now(), datetime.now()))
            
            customer_id = cursor.lastrowid
            self.conn.commit()
            
            logger.info(f"👤 New customer added: {email} (ID: {customer_id})")
            
            # Send welcome email
            await self.send_welcome_email(email, first_name)
            
            return customer_id
            
        except sqlite3.IntegrityError:
            # Customer already exists
            cursor.execute("SELECT id FROM customers WHERE email = ?", (email,))
            existing_id = cursor.fetchone()[0]
            logger.info(f"👤 Customer already exists: {email} (ID: {existing_id})")
            return existing_id
    
    async def record_purchase(self, customer_email: str, product_id: str, amount: int):
        """Record customer purchase"""
        cursor = self.conn.cursor()
        
        # Get or create customer
        customer_id = await self.add_customer(customer_email)
        
        # Record purchase
        cursor.execute("""
            INSERT INTO customer_purchases (customer_id, product_id, purchase_date, amount)
            VALUES (?, ?, ?, ?)
        """, (customer_id, product_id, datetime.now(), amount))
        
        # Update customer totals
        cursor.execute("""
            UPDATE customers 
            SET total_purchases = total_purchases + 1,
                total_spent = total_spent + ?,
                last_activity = ?
            WHERE id = ?
        """, (amount, datetime.now(), customer_id))
        
        self.conn.commit()
        
        logger.info(f"💰 Purchase recorded: {customer_email} - ${amount/100:.2f}")
        
        # Send purchase confirmation
        await self.send_purchase_confirmation(customer_email, product_id, amount)
    
    async def get_customer_analytics(self) -> Dict:
        """Get customer analytics data"""
        cursor = self.conn.cursor()
        
        # Total customers
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]
        
        # New customers this month
        cursor.execute("""
            SELECT COUNT(*) FROM customers 
            WHERE DATE(registration_date) >= DATE('now', 'start of month')
        """)
        new_customers_month = cursor.fetchone()[0]
        
        # Customer lifetime value
        cursor.execute("""
            SELECT AVG(total_spent), MAX(total_spent), MIN(total_spent)
            FROM customers WHERE total_spent > 0
        """)
        ltv_data = cursor.fetchone()
        avg_ltv = ltv_data[0] / 100 if ltv_data[0] else 0
        max_ltv = ltv_data[1] / 100 if ltv_data[1] else 0
        
        # Top customers
        cursor.execute("""
            SELECT email, first_name, last_name, total_purchases, total_spent
            FROM customers
            ORDER BY total_spent DESC
            LIMIT 10
        """)
        top_customers = cursor.fetchall()
        
        # Purchase frequency
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN total_purchases = 1 THEN 'One-time'
                    WHEN total_purchases BETWEEN 2 AND 5 THEN 'Regular'
                    ELSE 'VIP'
                END as segment,
                COUNT(*) as count
            FROM customers
            WHERE total_purchases > 0
            GROUP BY segment
        """)
        customer_segments = cursor.fetchall()
        
        return {
            "total_customers": total_customers,
            "new_customers_month": new_customers_month,
            "avg_customer_ltv": round(avg_ltv, 2),
            "max_customer_ltv": round(max_ltv, 2),
            "top_customers": [
                {
                    "email": email,
                    "name": f"{first_name} {last_name}".strip(),
                    "purchases": purchases,
                    "total_spent": spent / 100
                }
                for email, first_name, last_name, purchases, spent in top_customers
            ],
            "customer_segments": [
                {"segment": segment, "count": count}
                for segment, count in customer_segments
            ]
        }
    
    async def send_welcome_email(self, email: str, first_name: str):
        """Send welcome email to new customer"""
        subject = "🎉 Welcome to Nosyt AI - Your AI Profit Journey Starts Now!"
        
        content = f"""
        Hi {first_name or 'there'}! 👋
        
        Welcome to the Nosyt AI family! 🤖
        
        You've just joined thousands of smart entrepreneurs who are using AI prompts to:
        
        ✨ Save 10+ hours per week
        💰 Generate consistent income  
        🚀 Scale their businesses faster
        📈 Get professional results instantly
        
        🎁 **Your Welcome Bonus:**
        • FREE Starter Pack: 10 High-Converting AI Prompts
        • AI Profit Blueprint (usually $97)
        • Access to our exclusive community
        • Daily profit tips and strategies
        
        Ready to start your AI-powered business?
        
        [CLAIM YOUR FREE STARTER PACK]
        
        To your success,
        Tyson @ Nosyt LLC
        New Mexico
        
        P.S. Keep an eye on your inbox - I'll be sharing my best AI profit secrets with you this week!
        
        ---
        Nosyt LLC | New Mexico | AI Automation Experts
        """
        
        await self.send_email(email, subject, content)
    
    async def send_purchase_confirmation(self, email: str, product_id: str, amount: int):
        """Send purchase confirmation email"""
        subject = f"✅ Your AI Prompt is Ready! (Order #{product_id[-8:]})"
        
        content = f"""
        Thank you for your purchase! 🎉
        
        Your AI prompt is ready for download:
        
        📦 **Order Details:**
        • Product: AI Prompt #{product_id[-8:]}
        • Amount: ${amount/100:.2f}
        • Order Date: {datetime.now().strftime('%B %d, %Y')}
        
        📥 **Download Instructions:**
        1. Check your downloads in your WHOP account
        2. Or click the direct download link below
        3. Save the file to your computer
        4. Copy the prompt and paste into ChatGPT/Claude
        
        [DOWNLOAD YOUR PROMPT NOW]
        
        📞 **Need Help?**
        Reply to this email or contact our support team.
        
        💡 **Pro Tip:**
        Join our Discord community to share results and get bonus prompts!
        
        Thanks for choosing Nosyt AI!
        
        Tyson @ Nosyt LLC
        
        ---
        Nosyt LLC | Professional AI Solutions
        """
        
        await self.send_email(email, subject, content)
    
    async def send_email(self, to_email: str, subject: str, content: str):
        """Send email (mock implementation)"""
        # In a real implementation, you'd use a proper email service like SendGrid, AWS SES, etc.
        logger.info(f"📧 Email sent to {to_email}: {subject}")
        
        # Mock email sending - in production you'd implement actual email sending
        # Example with Gmail SMTP (requires app password):
        """
        try:
            msg = MimeMultipart()
            msg['From'] = "noreply@nosyt.com"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MimeText(content, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("your-email@gmail.com", "your-app-password")
            text = msg.as_string()
            server.sendmail("noreply@nosyt.com", to_email, text)
            server.quit()
            
            logger.info(f"✅ Email sent successfully to {to_email}")
        except Exception as e:
            logger.error(f"❌ Email sending failed: {str(e)}")
        """
    
    async def create_support_ticket(self, customer_email: str, subject: str, message: str) -> int:
        """Create customer support ticket"""
        cursor = self.conn.cursor()
        
        # Get customer ID
        cursor.execute("SELECT id FROM customers WHERE email = ?", (customer_email,))
        result = cursor.fetchone()
        
        if not result:
            customer_id = await self.add_customer(customer_email)
        else:
            customer_id = result[0]
        
        # Create ticket
        cursor.execute("""
            INSERT INTO support_tickets (customer_id, subject, message, created_at)
            VALUES (?, ?, ?, ?)
        """, (customer_id, subject, message, datetime.now()))
        
        ticket_id = cursor.lastrowid
        self.conn.commit()
        
        logger.info(f"🎟️ Support ticket created: #{ticket_id} for {customer_email}")
        
        # Send auto-response
        await self.send_support_auto_response(customer_email, ticket_id)
        
        return ticket_id
    
    async def send_support_auto_response(self, email: str, ticket_id: int):
        """Send automatic support response"""
        subject = f"🎟️ Support Ticket #{ticket_id} - We're Here to Help!"
        
        content = f"""
        Thanks for contacting Nosyt AI support! 👋
        
        We've received your message and assigned it ticket #{ticket_id}.
        
        ⏱️ **Response Time:** Usually within 4-6 hours
        📞 **Priority Support:** Available for VIP customers
        
        **Common Solutions:**
        • Download issues? Check your WHOP account downloads
        • Prompt not working? Make sure you're using the exact text
        • Need customization? We offer custom prompt services
        
        **Helpful Resources:**
        • FAQ: [link]
        • Video Tutorials: [link]
        • Discord Community: [link]
        
        Our team will get back to you soon!
        
        Best regards,
        Nosyt AI Support Team
        
        ---
        Ticket ID: #{ticket_id}
        Nosyt LLC | Professional AI Solutions
        """
        
        await self.send_email(email, subject, content)
    
    async def get_customer_by_email(self, email: str) -> Optional[Dict]:
        """Get customer information by email"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT id, email, first_name, last_name, registration_date, 
                   total_purchases, total_spent, status, last_activity
            FROM customers WHERE email = ?
        """, (email,))
        
        result = cursor.fetchone()
        
        if result:
            return {
                "id": result[0],
                "email": result[1],
                "first_name": result[2],
                "last_name": result[3],
                "registration_date": result[4],
                "total_purchases": result[5],
                "total_spent": result[6] / 100,
                "status": result[7],
                "last_activity": result[8]
            }
        
        return None
    
    async def send_marketing_campaign(self, campaign_name: str, subject: str, content: str, target_segment: str = "all"):
        """Send marketing email campaign"""
        cursor = self.conn.cursor()
        
        # Get target customers based on segment
        if target_segment == "vip":
            cursor.execute("SELECT email FROM customers WHERE total_purchases >= 5")
        elif target_segment == "regular":
            cursor.execute("SELECT email FROM customers WHERE total_purchases BETWEEN 2 AND 4")
        elif target_segment == "new":
            cursor.execute("""
                SELECT email FROM customers 
                WHERE DATE(registration_date) >= DATE('now', '-30 days')
            """)
        else:  # all
            cursor.execute("SELECT email FROM customers WHERE status = 'active'")
        
        recipients = cursor.fetchall()
        recipients_count = len(recipients)
        
        # Record campaign
        cursor.execute("""
            INSERT INTO email_campaigns (campaign_name, subject, content, sent_at, recipients_count)
            VALUES (?, ?, ?, ?, ?)
        """, (campaign_name, subject, content, datetime.now(), recipients_count))
        
        self.conn.commit()
        
        # Send emails (in production, you'd use a proper email service)
        for (email,) in recipients:
            await self.send_email(email, subject, content)
        
        logger.info(f"📢 Marketing campaign '{campaign_name}' sent to {recipients_count} customers")
        
        return recipients_count
    
    async def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("📁 Customer database connection closed")