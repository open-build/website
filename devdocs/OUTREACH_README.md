# 🚀 Open Build Outreach Automation System

A comprehensive, ethical, and intelligent system for discovering and reaching out to potential partners, donors, and clients for Open Build's developer training programs.

## ✨ Features

### 🎯 Automated Target Discovery
- Scrapes startup publications, communities, and platforms
- Continuously discovers new targets each day
- Categorizes targets by type (startup, publication, influencer, community)
- Smart filtering to avoid duplicates and irrelevant targets

### 📧 Intelligent Outreach
- Personalized email templates for each target category
- Professional messaging highlighting Open Build's mission
- Brevo SMTP integration for reliable email delivery
- BCC to team@open.build on all outreach emails

### 🛡️ Ethical & Safe Operations
- **Rate Limiting**: 30-60 second delays between requests
- **Contact Limits**: Maximum 4 contacts per organization
- **Cooldown Period**: 30-day wait between repeat contacts
- **Robots.txt Compliance**: Respects website scraping policies
- **Daily Limits**: Maximum 15 emails per day

### 📊 Comprehensive Tracking
- SQLite database for all targets and outreach history
- Daily reports with statistics and summaries
- Email notifications for all activities
- Performance analytics and metrics

## 🚀 Quick Start

### 1. Setup the System
```bash
# Run the setup script
./setup_outreach.sh

# Or manually install dependencies
python3 -m venv outreach_env
source outreach_env/bin/activate
pip install -r requirements.txt
```

### 2. Test the Configuration
```bash
# Test email and database systems
python test_outreach_system.py
```

### 3. Generate Initial Report
```bash
# Check system status
python outreach_automation.py --report
```

### 4. Run Manual Outreach
```bash
# Run the daily automation manually
python outreach_automation.py --run
```

### 5. Enable Daily Automation

**On macOS:**
```bash
launchctl load ~/Library/LaunchAgents/com.openbuild.outreach.plist
```

**On Linux:**
```bash
sudo systemctl enable openbuild-outreach.service
sudo systemctl start openbuild-outreach.service
```

## 📋 System Architecture

### Core Components

1. **Target Discovery (`TargetDiscovery`)**: Finds new potential contacts
2. **Web Scraper (`WebScraper`)**: Ethically scrapes websites for contact info
3. **Database Manager (`DatabaseManager`)**: Handles all data operations
4. **Email Sender (`EmailSender`)**: Manages outreach emails via Brevo SMTP
5. **Message Templates (`MessageTemplates`)**: Personalizes messages by category

### Target Categories

- **🏢 Startups**: Early-stage companies needing developer training
- **📰 Publications**: Media outlets covering the startup ecosystem  
- **👤 Influencers**: Developer community leaders and content creators
- **🏘️ Communities**: Developer organizations and platforms
- **⚡ Platforms**: Developer tools and service providers

## 📧 Email Configuration

The system uses **Brevo SMTP** for reliable email delivery. All credentials are stored securely in environment variables:

**Environment Variables (.env file):**
```bash
BREVO_SMTP_HOST=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_USER=your_brevo_user
BREVO_SMTP_PASSWORD=your_brevo_password
FROM_EMAIL=team@open.build
FROM_NAME=Open Build Foundry Team
REPLY_TO_EMAIL=team@open.build
```

**🔒 Security Note**: Never commit the `.env` file to version control. The system loads these variables at runtime.

### Email Features
- ✅ Professional sender name and reply-to address
- ✅ Automatic BCC to team@open.build
- ✅ Category-specific personalized templates
- ✅ Daily summary reports
- ✅ Error notifications and logging

## 🎯 Message Templates

### Startup Outreach
Focuses on developer training services, junior developer onboarding, and corporate training solutions.

### Publication Outreach  
Emphasizes partnership opportunities, success stories, and content collaboration.

### Influencer Outreach
Highlights community impact, mentorship programs, and collaboration possibilities.

### Community Outreach
Emphasizes mutual support, workshop opportunities, and member benefits.

## 📊 Daily Workflow

1. **🔍 Discovery Phase**: Scan sources for new targets (5-10 new targets/day)
2. **📧 Outreach Phase**: Send personalized emails to qualified targets (max 15/day)
3. **📈 Reporting Phase**: Generate and send daily summary to team@open.build
4. **💾 Tracking Phase**: Update database with all activities and responses

## 🛠️ Configuration Options

### Rate Limiting
```json
{
  "limits": {
    "daily_emails": 15,
    "contacts_per_org": 4,
    "cooldown_days": 30,
    "delay_between_emails": [60, 120],
    "delay_between_requests": [30, 60]
  }
}
```

### Discovery Settings
```json
{
  "discovery": {
    "targets_per_run": 10,
    "sources_per_category": 2,
    "max_urls_per_source": 5
  }
}
```

## 📈 Monitoring & Reports

### Daily Reports Include:
- 📊 New targets discovered
- 📧 Emails sent with recipient details
- 🎯 Pipeline status and metrics
- 📈 Performance analytics
- ⚠️ Error reports and system status

### Command Line Reporting:
```bash
# Generate comprehensive report
python outreach_automation.py --report

# View recent activity
tail -f outreach_automation.log

# Check database status
sqlite3 outreach_automation.db "SELECT category, COUNT(*) FROM targets GROUP BY category;"
```

## 🔒 Security & Privacy

- ✅ No sensitive data stored in plain text
- ✅ Respects robots.txt and website policies
- ✅ Rate limiting prevents server overload
- ✅ Professional email practices
- ✅ Comprehensive logging for transparency
- ✅ Opt-out mechanisms in all emails

## 🚀 Scaling & Performance

### Current Capacity:
- **Daily Discovery**: 10-15 new targets
- **Daily Outreach**: 15 emails maximum
- **Database**: Scales to 10,000+ targets
- **Monthly Volume**: ~450 emails, ~300 new targets

### Performance Optimizations:
- Async web scraping for faster discovery
- Database indexing for quick queries
- Rate limiting prevents API blocks
- Efficient duplicate detection

## 🛠️ Troubleshooting

### Common Issues:

**Email Not Sending:**
```bash
# Test email configuration
python test_outreach_system.py
```

**Database Errors:**
```bash
# Check database integrity
sqlite3 outreach_automation.db ".schema"
```

**Rate Limiting Issues:**
- Increase delay settings in config.json
- Reduce daily_emails limit
- Check robots.txt compliance

## 📞 Support & Maintenance

### Log Files:
- `outreach_automation.log`: Main system log
- `logs/outreach_stdout.log`: Standard output
- `logs/outreach_stderr.log`: Error output

### Database Maintenance:
```bash
# Backup database
cp outreach_automation.db backup_$(date +%Y%m%d).db

# Clean old logs
find logs/ -name "*.log" -mtime +30 -delete
```

### Updates & Improvements:
The system is designed for continuous improvement. Key areas for enhancement:
- AI-powered personalization
- Advanced target scoring
- Response tracking and analytics
- Integration with CRM systems

## 🎯 Expected Results

### Month 1:
- 300+ new targets discovered
- 450+ personalized emails sent
- 15-30 initial responses expected
- 5-10 qualified partnership discussions

### Ongoing:
- Steady pipeline of qualified leads
- Improved targeting through analytics
- Growing database of potential partners
- Measurable increase in partnership opportunities

---

**Built with ❤️ by the Open Build Team**

For questions or support, contact: team@open.build
