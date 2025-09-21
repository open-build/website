#!/usr/bin/env python3
"""
Open Build Automation Dashboard Generator
Creates a comprehensive HTML report showing automation status, configuration, and logs
Includes data retention policies (30 days) and automatic cleanup
"""

import sqlite3
import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# Set working directory to parent folder
os.chdir(Path(__file__).parent.parent)

def clean_old_data():
    """Clean old data from database and reports (keep only last 30 days)"""
    try:
        conn = sqlite3.connect('outreach_automation.db')
        cursor = conn.cursor()
        
        # Calculate cutoff date (30 days ago)
        cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Clean old daily stats
        cursor.execute("DELETE FROM daily_stats WHERE date < ?", (cutoff_date,))
        deleted_stats = cursor.rowcount
        
        # Clean old outreach logs (keep last 30 days)
        cutoff_datetime = (datetime.now() - timedelta(days=30)).isoformat()
        cursor.execute("DELETE FROM outreach_log WHERE created_at < ?", (cutoff_datetime,))
        deleted_outreach = cursor.rowcount
        
        # Clean old responses
        cursor.execute("DELETE FROM responses WHERE created_at < ?", (cutoff_datetime,))
        deleted_responses = cursor.rowcount
        
        # Clean old analytics tracking
        cursor.execute("DELETE FROM analytics_tracking WHERE date < ?", (cutoff_date,))
        deleted_analytics = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"🧹 Cleaned old data: {deleted_stats} daily stats, {deleted_outreach} outreach logs, {deleted_responses} responses, {deleted_analytics} analytics")
        
        # Clean old report files (keep last 30 days)
        reports_dir = Path('reports')
        if reports_dir.exists():
            cutoff_timestamp = datetime.now() - timedelta(days=30)
            cleaned_reports = 0
            
            for file in reports_dir.glob('automation_dashboard_*.html'):
                if file.stat().st_mtime < cutoff_timestamp.timestamp():
                    file.unlink()
                    cleaned_reports += 1
            
            if cleaned_reports > 0:
                print(f"🧹 Cleaned {cleaned_reports} old report files")
        
    except Exception as e:
        print(f"❌ Error cleaning old data: {e}")

def load_env_vars():
    """Load and analyze environment variables from .env file"""
    env_vars = {}
    env_file = Path('.env')
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    
    # Check which variables are configured
    required_vars = {
        'BREVO_SMTP_HOST': 'Email server configuration',
        'BREVO_SMTP_USER': 'Email authentication',
        'BREVO_SMTP_PASSWORD': 'Email authentication',
        'FROM_EMAIL': 'Sender email address',
        'FROM_NAME': 'Sender display name',
        'REPLY_TO_EMAIL': 'Reply-to email address'
    }
    
    optional_vars = {
        'GOOGLE_ANALYTICS_API_KEY': 'Website analytics tracking',
        'GOOGLE_ANALYTICS_VIEW_ID': 'Website analytics tracking',
        'YOUTUBE_API_KEY': 'YouTube analytics tracking',
        'YOUTUBE_CHANNEL_ID': 'YouTube analytics tracking',
        'GITHUB_REPO': 'GitHub repository tracking',
        'OPENAI_API_KEY': 'Enhanced personalization',
        'SLACK_WEBHOOK_URL': 'Slack notifications',
        'DISCORD_WEBHOOK_URL': 'Discord notifications'
    }
    
    status = {
        'configured': {},
        'missing': {},
        'optional_configured': {},
        'optional_missing': {}
    }
    
    for var, description in required_vars.items():
        if var in env_vars and env_vars[var].strip():
            status['configured'][var] = {
                'value': env_vars[var] if 'PASSWORD' not in var else '[CONFIGURED]',
                'description': description
            }
        else:
            status['missing'][var] = description
    
    for var, description in optional_vars.items():
        if var in env_vars and env_vars[var].strip():
            status['optional_configured'][var] = {
                'value': env_vars[var] if 'KEY' not in var else '[CONFIGURED]',
                'description': description
            }
        else:
            status['optional_missing'][var] = description
    
    return status

def get_database_stats():
    """Get comprehensive database statistics"""
    try:
        conn = sqlite3.connect('outreach_automation.db')
        cursor = conn.cursor()
        
        # Get date ranges
        today = datetime.now().strftime('%Y-%m-%d')
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        stats = {
            'total_targets': 0,
            'targets_by_category': [],
            'daily_stats': [],
            'weekly_summary': {'targets': 0, 'emails': 0, 'responses': 0},
            'monthly_summary': {'targets': 0, 'emails': 0, 'responses': 0},
            'recent_outreach': [],
            'pending_targets': 0,
            'contacted_targets': 0
        }
        
        # Total targets
        cursor.execute("SELECT COUNT(*) FROM targets")
        stats['total_targets'] = cursor.fetchone()[0]
        
        # Targets by category
        cursor.execute("""
            SELECT category, COUNT(*) 
            FROM targets 
            GROUP BY category 
            ORDER BY COUNT(*) DESC
        """)
        stats['targets_by_category'] = cursor.fetchall()
        
        # Daily stats for last 30 days
        cursor.execute("""
            SELECT date, new_targets_found, emails_sent, responses_received, total_targets
            FROM daily_stats 
            WHERE date >= ? 
            ORDER BY date DESC
        """, (month_ago,))
        stats['daily_stats'] = cursor.fetchall()
        
        # Weekly summary
        cursor.execute("""
            SELECT 
                COALESCE(SUM(new_targets_found), 0) as targets,
                COALESCE(SUM(emails_sent), 0) as emails,
                COALESCE(SUM(responses_received), 0) as responses
            FROM daily_stats 
            WHERE date >= ?
        """, (week_ago,))
        result = cursor.fetchone()
        if result:
            stats['weekly_summary'] = {
                'targets': result[0],
                'emails': result[1], 
                'responses': result[2]
            }
        
        # Monthly summary
        cursor.execute("""
            SELECT 
                COALESCE(SUM(new_targets_found), 0) as targets,
                COALESCE(SUM(emails_sent), 0) as emails,
                COALESCE(SUM(responses_received), 0) as responses
            FROM daily_stats 
            WHERE date >= ?
        """, (month_ago,))
        result = cursor.fetchone()
        if result:
            stats['monthly_summary'] = {
                'targets': result[0],
                'emails': result[1],
                'responses': result[2]
            }
        
        # Recent outreach attempts
        cursor.execute("""
            SELECT t.name, t.email, t.category, ol.subject, ol.status, ol.created_at
            FROM outreach_log ol
            JOIN targets t ON ol.target_id = t.id
            ORDER BY ol.created_at DESC
            LIMIT 20
        """)
        stats['recent_outreach'] = cursor.fetchall()
        
        # Pending targets (ready for outreach)
        cooldown_date = (datetime.now() - timedelta(days=30)).isoformat()
        cursor.execute("""
            SELECT COUNT(*) FROM targets 
            WHERE contact_count < 4 
            AND (last_contacted IS NULL OR last_contacted < ?)
            AND email IS NOT NULL AND email != ''
        """, (cooldown_date,))
        stats['pending_targets'] = cursor.fetchone()[0]
        
        # Already contacted targets
        cursor.execute("""
            SELECT COUNT(*) FROM targets 
            WHERE last_contacted IS NOT NULL
        """)
        stats['contacted_targets'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
        
    except Exception as e:
        print(f"Database error: {e}")
        return None

def get_log_files():
    """Get recent log file contents"""
    logs = {}
    log_files = {
        'cron.log': 'Cron Job Execution Log',
        'daily_automation.log': 'Daily Automation Output',
        'daily_automation_errors.log': 'Daily Automation Errors',
        'weekly_analytics.log': 'Weekly Analytics Output',
        'weekly_analytics_errors.log': 'Weekly Analytics Errors'
    }
    
    for file, description in log_files.items():
        file_path = Path('logs') / file
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Get last 50 lines or last 5000 characters
                    lines = content.split('\n')
                    if len(lines) > 50:
                        content = '\n'.join(lines[-50:])
                    elif len(content) > 5000:
                        content = content[-5000:]
                    
                    logs[file] = {
                        'description': description,
                        'content': content,
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    }
            except Exception as e:
                logs[file] = {
                    'description': description,
                    'content': f'Error reading file: {e}',
                    'size': 0,
                    'modified': 'Unknown'
                }
        else:
            logs[file] = {
                'description': description,
                'content': 'File not found',
                'size': 0,
                'modified': 'N/A'
            }
    
    return logs

def generate_html_report():
    """Generate comprehensive HTML report with data retention"""
    
    print("🔍 Gathering data for automation report...")
    
    # First, clean old data
    clean_old_data()
    
    # Collect all data
    env_status = load_env_vars()
    db_stats = get_database_stats()
    logs = get_log_files()
    
    if not db_stats:
        print("❌ Could not access database - generating limited report")
        db_stats = {
            'total_targets': 0, 'targets_by_category': [], 'daily_stats': [],
            'weekly_summary': {'targets': 0, 'emails': 0, 'responses': 0},
            'monthly_summary': {'targets': 0, 'emails': 0, 'responses': 0},
            'recent_outreach': [], 'pending_targets': 0, 'contacted_targets': 0
        }
    
    # Generate timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f'automation_dashboard_{timestamp}.html'
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Build Automation Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header .subtitle {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #3498db;
        }}
        
        .card.success {{ border-left-color: #27ae60; }}
        .card.warning {{ border-left-color: #f39c12; }}
        .card.error {{ border-left-color: #e74c3c; }}
        
        .card h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        .metric:last-child {{
            border-bottom: none;
        }}
        
        .metric-value {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .status-indicator {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        .status-indicator.green {{ background: #27ae60; }}
        .status-indicator.yellow {{ background: #f39c12; }}
        .status-indicator.red {{ background: #e74c3c; }}
        
        .table-container {{
            overflow-x: auto;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        
        th {{
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 500;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .log-section {{
            margin: 30px 0;
        }}
        
        .log-tabs {{
            display: flex;
            border-bottom: 2px solid #ecf0f1;
            margin-bottom: 20px;
        }}
        
        .log-tab {{
            padding: 10px 20px;
            background: #ecf0f1;
            border: none;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }}
        
        .log-tab.active {{
            background: #3498db;
            color: white;
        }}
        
        .log-content {{
            display: none;
        }}
        
        .log-content.active {{
            display: block;
        }}
        
        .log-box {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
        }}
        
        .env-section {{
            margin: 30px 0;
        }}
        
        .env-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .env-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: white;
            border-radius: 5px;
            border-left: 3px solid #ecf0f1;
        }}
        
        .env-item.configured {{ border-left-color: #27ae60; }}
        .env-item.missing {{ border-left-color: #e74c3c; }}
        
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 20px;
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .env-grid {{
                grid-template-columns: 1fr;
            }}
            
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Open Build Automation Dashboard</h1>
            <div class="subtitle">Real-time monitoring and configuration status</div>
        </div>
        
        <div class="content">
            <!-- Summary Cards -->
            <div class="dashboard-grid">
                <div class="card success">
                    <h3>📊 Overall Status</h3>
                    <div class="metric">
                        <span>Total Targets</span>
                        <span class="metric-value">{db_stats['total_targets']}</span>
                    </div>
                    <div class="metric">
                        <span>Targets Contacted</span>
                        <span class="metric-value">{db_stats['contacted_targets']}</span>
                    </div>
                    <div class="metric">
                        <span>Ready for Outreach</span>
                        <span class="metric-value">{db_stats['pending_targets']}</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3>📅 Last 7 Days</h3>
                    <div class="metric">
                        <span>New Targets</span>
                        <span class="metric-value">{db_stats['weekly_summary']['targets']}</span>
                    </div>
                    <div class="metric">
                        <span>Emails Sent</span>
                        <span class="metric-value">{db_stats['weekly_summary']['emails']}</span>
                    </div>
                    <div class="metric">
                        <span>Responses</span>
                        <span class="metric-value">{db_stats['weekly_summary']['responses']}</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3>📅 Last 30 Days</h3>
                    <div class="metric">
                        <span>New Targets</span>
                        <span class="metric-value">{db_stats['monthly_summary']['targets']}</span>
                    </div>
                    <div class="metric">
                        <span>Emails Sent</span>
                        <span class="metric-value">{db_stats['monthly_summary']['emails']}</span>
                    </div>
                    <div class="metric">
                        <span>Responses</span>
                        <span class="metric-value">{db_stats['monthly_summary']['responses']}</span>
                    </div>
                </div>
                
                <div class="card {'success' if len(env_status['missing']) == 0 else 'warning'}">
                    <h3>⚙️ Configuration Status</h3>
                    <div class="metric">
                        <span>Required Settings</span>
                        <span class="metric-value">
                            <span class="status-indicator {'green' if len(env_status['missing']) == 0 else 'red'}"></span>
                            {len(env_status['configured'])}/{len(env_status['configured']) + len(env_status['missing'])}
                        </span>
                    </div>
                    <div class="metric">
                        <span>Optional Features</span>
                        <span class="metric-value">
                            <span class="status-indicator {'green' if len(env_status['optional_configured']) > 0 else 'yellow'}"></span>
                            {len(env_status['optional_configured'])}/{len(env_status['optional_configured']) + len(env_status['optional_missing'])}
                        </span>
                    </div>
                </div>
            </div>
            
            <!-- Target Categories -->
            {"<div class='card'><h3>🎯 Targets by Category</h3>" if db_stats['targets_by_category'] else ""}
            {"".join([f"<div class='metric'><span>{category.title()}</span><span class='metric-value'>{count}</span></div>" for category, count in db_stats['targets_by_category']])}
            {"</div>" if db_stats['targets_by_category'] else ""}
            
            <!-- Daily Stats Table -->
            <div class="table-container">
                <h3 style="margin-bottom: 15px;">📈 Daily Activity (Last 30 Days)</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>New Targets</th>
                            <th>Emails Sent</th>
                            <th>Responses</th>
                            <th>Total Targets</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Add daily stats rows
    for stat in db_stats['daily_stats'][:30]:  # Last 30 days
        html_content += f"""
                        <tr>
                            <td>{stat[0]}</td>
                            <td>{stat[1]}</td>
                            <td>{stat[2]}</td>
                            <td>{stat[3]}</td>
                            <td>{stat[4]}</td>
                        </tr>
"""

    html_content += """
                    </tbody>
                </table>
            </div>
            
            <!-- Recent Outreach -->
"""

    if db_stats['recent_outreach']:
        html_content += """
            <div class="table-container">
                <h3 style="margin-bottom: 15px;">📧 Recent Outreach</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Target</th>
                            <th>Email</th>
                            <th>Category</th>
                            <th>Subject</th>
                            <th>Status</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for outreach in db_stats['recent_outreach']:
            html_content += f"""
                        <tr>
                            <td>{outreach[0]}</td>
                            <td>{outreach[1]}</td>
                            <td>{outreach[2]}</td>
                            <td>{outreach[3]}</td>
                            <td>{outreach[4]}</td>
                            <td>{outreach[5][:16]}</td>
                        </tr>
"""
        html_content += """
                    </tbody>
                </table>
            </div>
"""

    # Environment Configuration Section
    html_content += """
            <!-- Environment Configuration -->
            <div class="env-section">
                <h3>⚙️ Environment Configuration</h3>
                <div class="env-grid">
                    <div class="card">
                        <h4>✅ Required Settings (Configured)</h4>
"""

    for var, config in env_status['configured'].items():
        html_content += f"""
                        <div class="env-item configured">
                            <div>
                                <strong>{var}</strong><br>
                                <small>{config['description']}</small>
                            </div>
                            <span>✓ {config['value']}</span>
                        </div>
"""

    html_content += """
                    </div>
                    <div class="card">
                        <h4>❌ Required Settings (Missing)</h4>
"""

    for var, description in env_status['missing'].items():
        html_content += f"""
                        <div class="env-item missing">
                            <div>
                                <strong>{var}</strong><br>
                                <small>{description}</small>
                            </div>
                            <span>❌ Not Set</span>
                        </div>
"""

    if not env_status['missing']:
        html_content += """
                        <div class="env-item configured">
                            <div>All required settings are configured!</div>
                            <span>✅</span>
                        </div>
"""

    html_content += """
                    </div>
                </div>
                
                <div class="env-grid" style="margin-top: 20px;">
                    <div class="card">
                        <h4>🔧 Optional Features (Configured)</h4>
"""

    for var, config in env_status['optional_configured'].items():
        html_content += f"""
                        <div class="env-item configured">
                            <div>
                                <strong>{var}</strong><br>
                                <small>{config['description']}</small>
                            </div>
                            <span>✓ {config['value']}</span>
                        </div>
"""

    if not env_status['optional_configured']:
        html_content += """
                        <div class="env-item missing">
                            <div>No optional features configured</div>
                            <span>-</span>
                        </div>
"""

    html_content += """
                    </div>
                    <div class="card">
                        <h4>⚠️ Optional Features (Available)</h4>
"""

    for var, description in env_status['optional_missing'].items():
        html_content += f"""
                        <div class="env-item missing">
                            <div>
                                <strong>{var}</strong><br>
                                <small>{description}</small>
                            </div>
                            <span>○ Available</span>
                        </div>
"""

    html_content += """
                    </div>
                </div>
            </div>
            
            <!-- Log Files Section -->
            <div class="log-section">
                <h3>📋 System Logs</h3>
                <div class="log-tabs">
"""

    # Create log tabs
    first_tab = True
    for filename, log_data in logs.items():
        active_class = "active" if first_tab else ""
        html_content += f'<button class="log-tab {active_class}" onclick="showLog(\'{filename}\')">{log_data["description"]}</button>'
        first_tab = False

    html_content += """
                </div>
"""

    # Create log content areas
    first_content = True
    for filename, log_data in logs.items():
        active_class = "active" if first_content else ""
        html_content += f"""
                <div id="{filename}" class="log-content {active_class}">
                    <div style="margin-bottom: 10px;">
                        <strong>File:</strong> logs/{filename} | 
                        <strong>Size:</strong> {log_data['size']} bytes | 
                        <strong>Modified:</strong> {log_data['modified']}
                    </div>
                    <div class="log-box">{log_data['content'] if log_data['content'] else 'No content'}</div>
                </div>
"""
        first_content = False

    html_content += f"""
            </div>
            
            <div class="timestamp">
                📅 Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    </div>
    
    <script>
        function showLog(logId) {{
            // Hide all log contents
            const contents = document.querySelectorAll('.log-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.log-tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected log content
            document.getElementById(logId).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
"""

    # Write the HTML file
    report_path = Path('reports') / report_filename
    with open(report_path, 'w') as f:
        f.write(html_content)
    
    # Also create/update the main dashboard file
    main_dashboard = Path('reports') / 'automation_dashboard.html'
    with open(main_dashboard, 'w') as f:
        f.write(html_content)
    
    return report_path, main_dashboard

if __name__ == "__main__":
    print("🚀 Generating Open Build Automation Dashboard...")
    timestamped_report, main_report = generate_html_report()
    print(f"✅ Dashboard generated:")
    print(f"   📊 Main dashboard: {main_report.absolute()}")
    print(f"   📁 Timestamped copy: {timestamped_report.absolute()}")
    print(f"🌐 Open in browser: file://{main_report.absolute()}")