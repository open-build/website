# Open Build Automation System - Architecture Documentation

## 📁 Project Structure

```
open-build-new-website/
├── 📝 devdocs/                    # Documentation
│   ├── ARCHITECTURE.md            # This file - system architecture
│   ├── CRON_SETUP_COMPLETE.md    # Cron job setup guide
│   ├── ENHANCED_FEATURES.md       # Feature documentation
│   └── OUTREACH_README.md         # Outreach system guide
├── 📊 reports/                    # Generated reports (30-day retention)
│   ├── generate_report.py         # Dashboard generator script
│   ├── automation_dashboard.html  # Latest dashboard
│   └── automation_dashboard_*.html # Historical reports
├── 🔧 scripts/                    # Automation scripts
│   ├── outreach_automation.py     # Main automation engine
│   ├── run_daily_automation.sh    # Daily cron job script
│   ├── run_weekly_analytics.sh    # Weekly analytics script
│   ├── monitor_automation.sh      # System monitoring script
│   ├── setup_cron.sh              # Cron job setup script
│   └── test_*.py                  # Testing scripts
├── 📈 logs/                       # System logs (30-day retention)
│   ├── cron.log                   # Cron execution log
│   ├── daily_automation.log       # Daily automation output
│   ├── daily_automation_errors.log # Error log
│   ├── weekly_analytics.log       # Weekly analytics output
│   └── weekly_analytics_errors.log # Weekly analytics errors
├── 💾 outreach_automation.db      # SQLite database
├── ⚙️ .env                        # Environment configuration
└── 🌐 website files...           # Static website assets
```

## 🏗️ System Architecture

### Core Components

1. **Main Automation Engine** (`scripts/outreach_automation.py`)
   - Target discovery and management
   - Email campaign execution
   - Analytics collection
   - Database operations
   - Data retention policies

2. **Report Generation** (`reports/generate_report.py`)
   - HTML dashboard creation
   - Configuration status monitoring
   - Log file analysis
   - Historical data visualization

3. **Cron Job Automation** (`scripts/*.sh`)
   - Daily outreach execution (9:00 AM)
   - Weekly analytics reporting (Sunday 8:00 AM)
   - Monthly data cleanup (1st of month 2:00 AM)
   - System monitoring and alerts

### Database Schema

```sql
-- Targets: Potential outreach contacts
CREATE TABLE targets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    email TEXT,
    contact_name TEXT,
    contact_role TEXT,
    description TEXT,
    last_contacted TEXT,
    contact_count INTEGER DEFAULT 0,
    priority INTEGER DEFAULT 1,
    notes TEXT,
    created_at TEXT,
    updated_at TEXT
);

-- Outreach Log: Email campaign tracking
CREATE TABLE outreach_log (
    id INTEGER PRIMARY KEY,
    target_id INTEGER,
    email_sent TEXT,
    subject TEXT,
    message_template TEXT,
    status TEXT,
    response_received TEXT,
    created_at TEXT,
    FOREIGN KEY (target_id) REFERENCES targets (id)
);

-- Daily Stats: Performance metrics
CREATE TABLE daily_stats (
    date TEXT PRIMARY KEY,
    new_targets_found INTEGER DEFAULT 0,
    emails_sent INTEGER DEFAULT 0,
    responses_received INTEGER DEFAULT 0,
    total_targets INTEGER DEFAULT 0
);

-- Additional tables: responses, discovered_sources, analytics_tracking
```

## 🔄 Data Flow

1. **Daily Automation Process**
   ```
   Target Discovery → Email Campaign → Analytics Collection → Report Generation
   ```

2. **Data Retention**
   - Database records: 30 days
   - Log files: 30 days  
   - Report files: 30 days
   - Automatic cleanup on each run

3. **Monitoring & Alerting**
   - Real-time error notifications
   - Weekly summary reports
   - Dashboard updates
   - System health checks

## ⚙️ Configuration Management

### Required Environment Variables
```bash
# Email Configuration
BREVO_SMTP_HOST=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_USER=your_smtp_user
BREVO_SMTP_PASSWORD=your_smtp_password
FROM_EMAIL=team@open.build
FROM_NAME=Open Build Foundry Team
REPLY_TO_EMAIL=team@open.build
```

### Optional Integrations
```bash
# Analytics APIs
GOOGLE_ANALYTICS_API_KEY=your_ga_key
GOOGLE_ANALYTICS_VIEW_ID=your_view_id
YOUTUBE_API_KEY=your_youtube_key
YOUTUBE_CHANNEL_ID=your_channel_id

# Notifications
SLACK_WEBHOOK_URL=your_slack_webhook
DISCORD_WEBHOOK_URL=your_discord_webhook
```

## 🚀 Deployment & Operations

### Initial Setup
```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 2. Set up automation
cd scripts/
./setup_cron.sh

# 3. Generate first report
cd ../reports/
python3 generate_report.py
```

### Daily Operations
- System runs automatically via cron jobs
- Monitor dashboard at `reports/automation_dashboard.html`
- Check logs in `logs/` directory
- Receive email reports automatically

### Maintenance Tasks
- Review target categories monthly
- Update email templates quarterly
- Monitor response rates and adjust strategy
- Review and update documentation

## 📊 Performance Metrics

### Key Performance Indicators (KPIs)
- **Target Discovery Rate**: New targets found per day
- **Email Delivery Rate**: Successful email sends
- **Response Rate**: Replies received from outreach
- **Pipeline Growth**: Total targets in database
- **System Uptime**: Automation reliability

### Monitoring Thresholds
- Daily emails: 15 maximum (rate limiting)
- Contact frequency: 30-day cooldown
- Database size: Automatic cleanup at 30 days
- Error rate: Alerts on consecutive failures

## 🔒 Security & Privacy

### Data Protection
- Environment variables for sensitive data
- Local SQLite database (no cloud storage)
- Rate limiting to prevent spam accusations
- Respect for robots.txt and rate limits

### Email Compliance
- Professional sender reputation
- Clear unsubscribe mechanisms
- Authentic sender identification
- GDPR compliance considerations

## 🛠️ Troubleshooting

### Common Issues
1. **No emails being sent**: Check environment variables
2. **Database errors**: Verify file permissions
3. **Cron not running**: Check crontab installation
4. **Low target discovery**: Review source accessibility

### Debug Commands
```bash
# Test automation manually
cd scripts/
python3 outreach_automation.py --run

# Check system status
./monitor_automation.sh

# Generate fresh report
cd ../reports/
python3 generate_report.py

# View recent logs
tail -f ../logs/daily_automation_errors.log
```

## 📈 Future Enhancements

### Planned Features
- AI-powered email personalization
- Advanced analytics dashboard
- Multi-channel outreach (LinkedIn, Twitter)
- Response sentiment analysis
- A/B testing for email templates

### Integration Opportunities
- CRM system integration
- Advanced lead scoring
- Social media monitoring
- Website visitor tracking
- Automated follow-up sequences

---

**Last Updated**: September 21, 2025  
**Version**: 2.0  
**Maintainer**: Open Build Team