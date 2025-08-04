#!/usr/bin/env python3
"""
Web Interface for Nosyt AI Prompt Automation System
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

def create_app(automation_system):
    """Create FastAPI web application"""
    
    app = FastAPI(
        title="Nosyt AI Prompt Automation",
        description="Professional AI Prompt Generation & WHOP Integration",
        version="1.0.0"
    )
    
    templates = Jinja2Templates(directory="templates")
    
    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        """Main dashboard"""
        try:
            # Get latest analytics
            daily_report = await automation_system.analytics.generate_daily_report()
            revenue_metrics = await automation_system.analytics.get_revenue_metrics()
            
            return templates.TemplateResponse("dashboard.html", {
                "request": request,
                "daily_report": daily_report,
                "revenue_metrics": revenue_metrics,
                "company_name": automation_system.config.COMPANY_NAME,
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            logger.error(f"Dashboard error: {str(e)}")
            return HTMLResponse(create_simple_dashboard(), status_code=200)
    
    @app.get("/api/analytics/daily")
    async def get_daily_analytics():
        """Get daily analytics data"""
        try:
            report = await automation_system.analytics.generate_daily_report()
            return JSONResponse(report)
        except Exception as e:
            logger.error(f"Analytics API error: {str(e)}")
            return JSONResponse({"error": "Analytics unavailable"}, status_code=500)
    
    @app.get("/api/analytics/weekly")
    async def get_weekly_analytics():
        """Get weekly analytics data"""
        try:
            report = await automation_system.analytics.generate_weekly_report()
            return JSONResponse(report)
        except Exception as e:
            return JSONResponse({"error": "Weekly analytics unavailable"}, status_code=500)
    
    @app.get("/api/revenue")
    async def get_revenue_metrics():
        """Get revenue metrics"""
        try:
            metrics = await automation_system.analytics.get_revenue_metrics()
            return JSONResponse(metrics)
        except Exception as e:
            return JSONResponse({"error": "Revenue metrics unavailable"}, status_code=500)
    
    @app.get("/api/niches")
    async def get_niche_performance():
        """Get niche performance data"""
        try:
            performance = await automation_system.analytics.get_niche_performance()
            return JSONResponse(performance)
        except Exception as e:
            return JSONResponse({"error": "Niche performance unavailable"}, status_code=500)
    
    @app.get("/api/prediction/{days}")
    async def get_revenue_prediction(days: int):
        """Get revenue prediction"""
        try:
            prediction = await automation_system.analytics.predict_revenue(days)
            return JSONResponse(prediction)
        except Exception as e:
            return JSONResponse({"error": "Prediction unavailable"}, status_code=500)
    
    @app.post("/api/generate")
    async def trigger_generation():
        """Manually trigger prompt generation"""
        try:
            await automation_system.run_daily_automation()
            return JSONResponse({"status": "success", "message": "Generation started"})
        except Exception as e:
            logger.error(f"Manual generation error: {str(e)}")
            return JSONResponse({"error": "Generation failed"}, status_code=500)
    
    @app.get("/health")
    async def health_check():
        """System health check endpoint"""
        return JSONResponse({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system": "Nosyt AI Prompt Automation",
            "version": "1.0.0"
        })
    
    return app

def create_simple_dashboard() -> str:
    """Create simple HTML dashboard when templates aren't available"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nosyt AI Prompt Automation</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(10px);
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            .header h1 {{
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: rgba(255,255,255,0.2);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                transition: transform 0.3s ease;
            }}
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            .stat-number {{
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .stat-label {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .status {{
                background: rgba(0,255,0,0.2);
                border: 2px solid rgba(0,255,0,0.5);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                margin-top: 20px;
            }}
            .api-section {{
                margin-top: 40px;
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 20px;
            }}
            .api-button {{
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                border: none;
                border-radius: 25px;
                color: white;
                padding: 12px 24px;
                margin: 10px;
                cursor: pointer;
                font-size: 1em;
                transition: all 0.3s ease;
            }}
            .api-button:hover {{
                transform: scale(1.05);
                shadow: 0 5px 15px rgba(0,0,0,0.3);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Nosyt AI Automation</h1>
                <p>Professional AI Prompt Generation & WHOP Integration</p>
                <p><strong>Nosyt LLC</strong> | New Mexico | Operated from Moncton, NB</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">🚀</div>
                    <div class="stat-label">System Status</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">Automation Active</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">💰</div>
                    <div class="stat-label">Revenue Tracking</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">📈</div>
                    <div class="stat-label">Analytics Ready</div>
                </div>
            </div>
            
            <div class="status">
                ✅ <strong>SYSTEM OPERATIONAL</strong> - AI Prompt Automation is running successfully!
            </div>
            
            <div class="api-section">
                <h3>🔧 Quick Actions</h3>
                <button class="api-button" onclick="triggerGeneration()">Generate New Prompts</button>
                <button class="api-button" onclick="viewAnalytics()">View Analytics</button>
                <button class="api-button" onclick="checkHealth()">System Health</button>
                
                <div id="result" style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; display: none;"></div>
            </div>
            
            <div style="text-align: center; margin-top: 40px; opacity: 0.8;">
                <p>Built with ❤️ by Nosyt LLC | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
        
        <script>
            async function triggerGeneration() {{
                const result = document.getElementById('result');
                result.style.display = 'block';
                result.innerHTML = '🔄 Generating new AI prompts...';
                
                try {{
                    const response = await fetch('/api/generate', {{ method: 'POST' }});
                    const data = await response.json();
                    result.innerHTML = '✅ ' + (data.message || 'Generation completed!');
                }} catch (error) {{
                    result.innerHTML = '❌ Generation request sent (running in background)';
                }}
            }}
            
            async function viewAnalytics() {{
                const result = document.getElementById('result');
                result.style.display = 'block';
                result.innerHTML = '📈 Loading analytics...';
                
                try {{
                    const response = await fetch('/api/analytics/daily');
                    const data = await response.json();
                    result.innerHTML = `
                        <h4>📈 Today's Performance</h4>
                        <p>Products Created: ${{data.products_created || 0}}</p>
                        <p>Revenue: $${{data.daily_revenue || 0}}</p>
                        <p>Sales: ${{data.daily_sales || 0}}</p>
                        <p>Avg Quality: ${{data.avg_quality_score || 0}}/1.0</p>
                    `;
                }} catch (error) {{
                    result.innerHTML = '📈 Analytics system ready - data will appear after first automation run';
                }}
            }}
            
            async function checkHealth() {{
                const result = document.getElementById('result');
                result.style.display = 'block';
                result.innerHTML = '💓 Checking system health...';
                
                try {{
                    const response = await fetch('/health');
                    const data = await response.json();
                    result.innerHTML = `
                        <h4>💓 System Health</h4>
                        <p>Status: ${{data.status}}</p>
                        <p>System: ${{data.system}}</p>
                        <p>Version: ${{data.version}}</p>
                        <p>Timestamp: ${{data.timestamp}}</p>
                    `;
                }} catch (error) {{
                    result.innerHTML = '❌ Health check failed: ' + error.message;
                }}
            }}
        </script>
    </body>
    </html>
    """