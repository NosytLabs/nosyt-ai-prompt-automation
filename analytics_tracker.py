#!/usr/bin/env python3
"""
Analytics and Performance Tracking System
"""

import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class AnalyticsTracker:
    """Comprehensive analytics and performance tracking"""
    
    def __init__(self, config):
        self.config = config
        self.db_path = "nosyt_analytics.db"
        self.conn = None
        
    async def initialize(self):
        """Initialize analytics database"""
        self.conn = sqlite3.connect(self.db_path)
        await self.create_tables()
        logger.info("✅ Analytics system initialized")
    
    async def create_tables(self):
        """Create analytics database tables"""
        cursor = self.conn.cursor()
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                title TEXT,
                niche TEXT,
                quality_score REAL,
                price INTEGER,
                created_at TIMESTAMP,
                whop_product_id TEXT
            )
        """)
        
        # Sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                amount INTEGER,
                customer_email TEXT,
                sale_date TIMESTAMP,
                platform TEXT,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        # Performance metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                metric_name TEXT,
                metric_value REAL,
                recorded_at TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        # Daily summary table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_summary (
                date DATE PRIMARY KEY,
                products_created INTEGER,
                total_revenue INTEGER,
                total_sales INTEGER,
                avg_quality_score REAL,
                top_niche TEXT
            )
        """)
        
        self.conn.commit()
        logger.info("📁 Analytics database tables created")
    
    async def track_product_creation(self, product_ids: List[str]):
        """Track newly created products"""
        cursor = self.conn.cursor()
        
        for product_id in product_ids:
            # In a real implementation, you'd get this data from the creation process
            cursor.execute("""
                INSERT OR REPLACE INTO products 
                (id, title, niche, quality_score, price, created_at, whop_product_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product_id,
                f"AI Prompt #{product_id[-6:]}",
                "Business & Marketing",  # Would come from actual data
                0.85,  # Would come from actual data
                45,    # Would come from actual data
                datetime.now(),
                product_id
            ))
        
        self.conn.commit()
        logger.info(f"📊 Tracked {len(product_ids)} product creations")
    
    async def track_sale(self, product_id: str, amount: int, customer_email: str, platform: str = "whop"):
        """Track a sale"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO sales (product_id, amount, customer_email, sale_date, platform)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, amount, customer_email, datetime.now(), platform))
        
        self.conn.commit()
        logger.info(f"💰 Tracked sale: ${amount/100:.2f} for product {product_id}")
    
    async def generate_daily_report(self) -> Dict:
        """Generate daily performance report"""
        cursor = self.conn.cursor()
        today = datetime.now().date()
        
        # Products created today
        cursor.execute("""
            SELECT COUNT(*) FROM products WHERE DATE(created_at) = ?
        """, (today,))
        products_created = cursor.fetchone()[0]
        
        # Revenue today
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM sales WHERE DATE(sale_date) = ?
        """, (today,))
        daily_revenue = cursor.fetchone()[0]
        
        # Sales count today
        cursor.execute("""
            SELECT COUNT(*) FROM sales WHERE DATE(sale_date) = ?
        """, (today,))
        daily_sales = cursor.fetchone()[0]
        
        # Average quality score
        cursor.execute("""
            SELECT COALESCE(AVG(quality_score), 0) FROM products WHERE DATE(created_at) = ?
        """, (today,))
        avg_quality = cursor.fetchone()[0]
        
        # Top performing niche
        cursor.execute("""
            SELECT niche, COUNT(*) as count FROM products 
            WHERE DATE(created_at) = ? GROUP BY niche ORDER BY count DESC LIMIT 1
        """, (today,))
        top_niche_result = cursor.fetchone()
        top_niche = top_niche_result[0] if top_niche_result else "N/A"
        
        report = {
            "date": today.isoformat(),
            "products_created": products_created,
            "daily_revenue": daily_revenue / 100,  # Convert cents to dollars
            "daily_sales": daily_sales,
            "avg_quality_score": round(avg_quality, 2),
            "top_niche": top_niche,
            "conversion_rate": (daily_sales / max(products_created, 1)) * 100
        }
        
        # Store daily summary
        cursor.execute("""
            INSERT OR REPLACE INTO daily_summary 
            (date, products_created, total_revenue, total_sales, avg_quality_score, top_niche)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (today, products_created, daily_revenue, daily_sales, avg_quality, top_niche))
        
        self.conn.commit()
        
        logger.info(f"📈 Daily Report: {json.dumps(report, indent=2)}")
        return report
    
    async def generate_weekly_report(self) -> Dict:
        """Generate weekly performance report"""
        cursor = self.conn.cursor()
        week_ago = (datetime.now() - timedelta(days=7)).date()
        
        # Weekly totals
        cursor.execute("""
            SELECT 
                COUNT(*) as products,
                COALESCE(SUM(CASE WHEN s.amount IS NOT NULL THEN s.amount ELSE 0 END), 0) as revenue,
                COUNT(s.id) as sales,
                COALESCE(AVG(p.quality_score), 0) as avg_quality
            FROM products p
            LEFT JOIN sales s ON p.id = s.product_id
            WHERE DATE(p.created_at) >= ?
        """, (week_ago,))
        
        result = cursor.fetchone()
        
        # Top niches this week
        cursor.execute("""
            SELECT niche, COUNT(*) as count, COALESCE(AVG(quality_score), 0) as avg_quality
            FROM products WHERE DATE(created_at) >= ?
            GROUP BY niche ORDER BY count DESC LIMIT 5
        """, (week_ago,))
        
        top_niches = cursor.fetchall()
        
        # Performance trends
        cursor.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as daily_products,
                   COALESCE(AVG(quality_score), 0) as daily_quality
            FROM products WHERE DATE(created_at) >= ?
            GROUP BY DATE(created_at) ORDER BY date
        """, (week_ago,))
        
        daily_trends = cursor.fetchall()
        
        report = {
            "period": "7_days",
            "total_products": result[0],
            "total_revenue": result[1] / 100,
            "total_sales": result[2],
            "avg_quality_score": round(result[3], 2),
            "conversion_rate": (result[2] / max(result[0], 1)) * 100,
            "top_niches": [
                {"niche": niche, "count": count, "avg_quality": round(quality, 2)}
                for niche, count, quality in top_niches
            ],
            "daily_trends": [
                {"date": date, "products": products, "quality": round(quality, 2)}
                for date, products, quality in daily_trends
            ]
        }
        
        return report
    
    async def get_revenue_metrics(self) -> Dict:
        """Get comprehensive revenue metrics"""
        cursor = self.conn.cursor()
        
        # Total metrics
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT p.id) as total_products,
                COALESCE(SUM(s.amount), 0) as total_revenue,
                COUNT(s.id) as total_sales,
                COALESCE(AVG(p.quality_score), 0) as avg_quality
            FROM products p
            LEFT JOIN sales s ON p.id = s.product_id
        """)
        
        totals = cursor.fetchone()
        
        # Monthly revenue
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', sale_date) as month,
                SUM(amount) as revenue,
                COUNT(*) as sales
            FROM sales
            GROUP BY strftime('%Y-%m', sale_date)
            ORDER BY month DESC
            LIMIT 12
        """)
        
        monthly_revenue = cursor.fetchall()
        
        # Top performing products
        cursor.execute("""
            SELECT 
                p.title,
                p.niche,
                p.price,
                COUNT(s.id) as sales_count,
                COALESCE(SUM(s.amount), 0) as total_revenue
            FROM products p
            LEFT JOIN sales s ON p.id = s.product_id
            GROUP BY p.id
            ORDER BY total_revenue DESC
            LIMIT 10
        """)
        
        top_products = cursor.fetchall()
        
        return {
            "total_products": totals[0],
            "total_revenue": totals[1] / 100,
            "total_sales": totals[2],
            "avg_quality_score": round(totals[3], 2),
            "monthly_revenue": [
                {"month": month, "revenue": revenue/100, "sales": sales}
                for month, revenue, sales in monthly_revenue
            ],
            "top_products": [
                {
                    "title": title,
                    "niche": niche,
                    "price": price/100,
                    "sales_count": sales_count,
                    "total_revenue": total_revenue/100
                }
                for title, niche, price, sales_count, total_revenue in top_products
            ]
        }
    
    async def get_niche_performance(self) -> Dict:
        """Get performance metrics by niche"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                p.niche,
                COUNT(DISTINCT p.id) as products_count,
                COALESCE(AVG(p.quality_score), 0) as avg_quality,
                COALESCE(AVG(p.price), 0) as avg_price,
                COUNT(s.id) as total_sales,
                COALESCE(SUM(s.amount), 0) as total_revenue
            FROM products p
            LEFT JOIN sales s ON p.id = s.product_id
            GROUP BY p.niche
            ORDER BY total_revenue DESC
        """)
        
        niche_data = cursor.fetchall()
        
        return {
            "niche_performance": [
                {
                    "niche": niche,
                    "products_count": products_count,
                    "avg_quality_score": round(avg_quality, 2),
                    "avg_price": avg_price / 100,
                    "total_sales": total_sales,
                    "total_revenue": total_revenue / 100,
                    "conversion_rate": (total_sales / max(products_count, 1)) * 100
                }
                for niche, products_count, avg_quality, avg_price, total_sales, total_revenue in niche_data
            ]
        }
    
    async def predict_revenue(self, days_ahead: int = 30) -> Dict:
        """Simple revenue prediction based on trends"""
        cursor = self.conn.cursor()
        
        # Get last 30 days of data for trend analysis
        cursor.execute("""
            SELECT DATE(sale_date) as date, COALESCE(SUM(amount), 0) as daily_revenue
            FROM sales
            WHERE sale_date >= date('now', '-30 days')
            GROUP BY DATE(sale_date)
            ORDER BY date
        """)
        
        historical_data = cursor.fetchall()
        
        if len(historical_data) < 7:  # Need at least a week of data
            return {"prediction": "Insufficient data for prediction"}
        
        # Simple linear trend calculation
        revenues = [row[1] for row in historical_data]
        avg_daily_revenue = sum(revenues) / len(revenues)
        
        # Calculate trend (very simplified)
        if len(revenues) > 1:
            trend = (revenues[-1] - revenues[0]) / len(revenues)
        else:
            trend = 0
        
        predicted_revenue = (avg_daily_revenue + trend * days_ahead) * days_ahead
        
        return {
            "prediction_period_days": days_ahead,
            "historical_avg_daily_revenue": avg_daily_revenue / 100,
            "predicted_total_revenue": max(predicted_revenue / 100, 0),
            "confidence": "low" if len(historical_data) < 14 else "medium"
        }
    
    async def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("📁 Analytics database connection closed")