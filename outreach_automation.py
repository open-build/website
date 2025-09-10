#!/usr/bin/env python3
"""
🚀 Open Build Startup Outreach Automation System

A comprehensive system for discovering and reaching out to potential partners,
donors, and clients for Open Build's developer training programs.

Features:
- Automated target discovery from multiple sources
- Smart contact extraction with rate limiting
- Personalized messaging based on target type
- Email integration with team@open.build
- Comprehensive tracking and reporting
- Ethical scraping with respect for robots.txt

Author: Open Build Team
License: MIT
"""

import asyncio
import aiohttp
import smtplib
import sqlite3
import json
import time
import random
import re
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import os
from pathlib import Path
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('outreach_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Target:
    """Represents a potential outreach target"""
    name: str
    url: str
    category: str  # publication, influencer, platform, community, startup
    email: str = ""
    contact_name: str = ""
    contact_role: str = ""
    description: str = ""
    last_contacted: Optional[str] = None
    contact_count: int = 0
    priority: int = 1  # 1-5 scale
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""

class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_path: str = "outreach_automation.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Targets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            )
        """)
        
        # Outreach log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outreach_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                email_sent TEXT,
                subject TEXT,
                message_template TEXT,
                status TEXT,
                response_received TEXT,
                created_at TEXT,
                FOREIGN KEY (target_id) REFERENCES targets (id)
            )
        """)
        
        # Daily stats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT PRIMARY KEY,
                new_targets_found INTEGER DEFAULT 0,
                emails_sent INTEGER DEFAULT 0,
                responses_received INTEGER DEFAULT 0,
                total_targets INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def add_target(self, target: Target) -> bool:
        """Add a new target to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            now = datetime.now().isoformat()
            target.created_at = now
            target.updated_at = now
            
            cursor.execute("""
                INSERT OR IGNORE INTO targets 
                (name, url, category, email, contact_name, contact_role, 
                 description, priority, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (target.name, target.url, target.category, target.email,
                  target.contact_name, target.contact_role, target.description,
                  target.priority, target.created_at, target.updated_at))
            
            success = cursor.rowcount > 0
            conn.commit()
            return success
        except Exception as e:
            logger.error(f"Error adding target: {e}")
            return False
        finally:
            conn.close()
    
    def get_targets_for_outreach(self, limit: int = 10) -> List[Target]:
        """Get targets ready for outreach (respecting cooldown periods)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cooldown_date = (datetime.now() - timedelta(days=30)).isoformat()
        
        cursor.execute("""
            SELECT * FROM targets 
            WHERE contact_count < 4 
            AND (last_contacted IS NULL OR last_contacted < ?)
            AND email IS NOT NULL AND email != ''
            ORDER BY priority DESC, created_at ASC
            LIMIT ?
        """, (cooldown_date, limit))
        
        targets = []
        for row in cursor.fetchall():
            target = Target(
                name=row[1], url=row[2], category=row[3], email=row[4],
                contact_name=row[5], contact_role=row[6], description=row[7],
                last_contacted=row[8], contact_count=row[9], priority=row[10],
                notes=row[11], created_at=row[12], updated_at=row[13]
            )
            targets.append(target)
        
        conn.close()
        return targets
    
    def update_contact_status(self, target_url: str, email_sent: bool = True):
        """Update target after contact attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            UPDATE targets 
            SET last_contacted = ?, contact_count = contact_count + 1, updated_at = ?
            WHERE url = ?
        """, (now, now, target_url))
        
        conn.commit()
        conn.close()
    
    def log_outreach(self, target_id: int, subject: str, template: str, status: str):
        """Log outreach attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO outreach_log 
            (target_id, subject, message_template, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (target_id, subject, template, status, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

class WebScraper:
    """Handles web scraping with ethical practices"""
    
    def __init__(self):
        self.session = None
        self.user_agent = "OpenBuild-Outreach-Bot/1.0 (+https://open.build)"
        self.delay_range = (30, 60)  # seconds between requests
    
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=2)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'User-Agent': self.user_agent}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def can_fetch(self, url: str) -> bool:
        """Check robots.txt compliance"""
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            return rp.can_fetch(self.user_agent, url)
        except:
            return True  # If robots.txt can't be fetched, assume allowed
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a web page with rate limiting and error handling"""
        if not self.can_fetch(url):
            logger.warning(f"Robots.txt disallows fetching: {url}")
            return None
        
        try:
            await asyncio.sleep(random.uniform(*self.delay_range))
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_emails(self, html: str) -> List[str]:
        """Extract email addresses from HTML"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html, re.IGNORECASE)
        
        # Filter out common non-contact emails
        filtered_emails = []
        skip_patterns = ['noreply', 'no-reply', 'donotreply', 'support', 'info@example']
        
        for email in emails:
            if not any(pattern in email.lower() for pattern in skip_patterns):
                filtered_emails.append(email.lower())
        
        return list(set(filtered_emails))  # Remove duplicates
    
    def extract_contact_info(self, html: str, base_url: str) -> Dict[str, str]:
        """Extract contact information from HTML"""
        contact_info = {'emails': [], 'names': [], 'roles': []}
        
        # Extract emails
        contact_info['emails'] = self.extract_emails(html)
        
        # Extract names (basic pattern matching)
        name_patterns = [
            r'CEO[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)',
            r'Founder[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)',
            r'Contact[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)',
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            contact_info['names'].extend(matches)
        
        return contact_info

class TargetDiscovery:
    """Discovers potential targets from various sources"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.sources = {
            'startup_publications': [
                'https://techcrunch.com',
                'https://venturebeat.com',
                'https://www.producthunt.com',
                'https://angel.co',
                'https://www.crunchbase.com'
            ],
            'developer_communities': [
                'https://dev.to',
                'https://hashnode.com',
                'https://medium.com/tag/programming',
                'https://reddit.com/r/programming',
                'https://news.ycombinator.com'
            ],
            'startup_directories': [
                'https://www.startupgrind.com',
                'https://f6s.com',
                'https://wellfound.com',
                'https://www.startupnation.com'
            ]
        }
    
    async def discover_targets(self) -> List[Target]:
        """Main target discovery method"""
        new_targets = []
        
        async with WebScraper() as scraper:
            for category, urls in self.sources.items():
                for url in urls[:2]:  # Limit to 2 sources per category per run
                    targets = await self._discover_from_source(scraper, url, category)
                    new_targets.extend(targets)
                    
                    # Respect rate limiting
                    await asyncio.sleep(random.uniform(30, 60))
        
        logger.info(f"Discovered {len(new_targets)} new targets")
        return new_targets
    
    async def _discover_from_source(self, scraper: WebScraper, url: str, category: str) -> List[Target]:
        """Discover targets from a specific source"""
        targets = []
        
        try:
            html = await scraper.fetch_page(url)
            if not html:
                return targets
            
            # Extract potential target URLs (simplified - would need source-specific logic)
            url_pattern = r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
            found_urls = re.findall(url_pattern, html)
            
            # Process a limited number of URLs
            for target_url in found_urls[:5]:
                if self._is_potential_target(target_url):
                    target = await self._analyze_target(scraper, target_url, category)
                    if target:
                        targets.append(target)
        
        except Exception as e:
            logger.error(f"Error discovering from {url}: {e}")
        
        return targets
    
    def _is_potential_target(self, url: str) -> bool:
        """Determine if a URL is a potential target"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Skip known non-targets
        skip_domains = ['google.com', 'facebook.com', 'twitter.com', 'linkedin.com']
        if any(skip in domain for skip in skip_domains):
            return False
        
        # Look for startup/business indicators
        business_indicators = ['startup', 'company', 'corp', 'inc', 'llc', 'ltd']
        return any(indicator in domain for indicator in business_indicators)
    
    async def _analyze_target(self, scraper: WebScraper, url: str, category: str) -> Optional[Target]:
        """Analyze a potential target URL"""
        try:
            html = await scraper.fetch_page(url)
            if not html:
                return None
            
            contact_info = scraper.extract_contact_info(html, url)
            
            # Extract company name from title or domain
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
            name = title_match.group(1).strip() if title_match else urlparse(url).netloc
            
            # Create target if we found contact info
            if contact_info['emails']:
                target = Target(
                    name=name,
                    url=url,
                    category=category,
                    email=contact_info['emails'][0],
                    contact_name=contact_info['names'][0] if contact_info['names'] else "",
                    description=f"Discovered from {category}",
                    priority=2
                )
                return target
        
        except Exception as e:
            logger.error(f"Error analyzing target {url}: {e}")
        
        return None

class MessageTemplates:
    """Manages personalized message templates"""
    
    @staticmethod
    def get_template(category: str, target: Target) -> Tuple[str, str]:
        """Get subject and message template for a target category"""
        
        templates = {
            'startup_publications': {
                'subject': f"Partnership Opportunity: Open Build + {target.name}",
                'message': f"""Hi {target.contact_name or 'there'},

I hope this email finds you well. I'm reaching out from Open Build, a nonprofit organization dedicated to training and mentoring junior developers in partnership with Buildly Labs.

We've been following {target.name}'s excellent work in the startup ecosystem, and I believe there's a valuable partnership opportunity worth exploring.

**What We Offer:**
• Comprehensive junior developer training programs
• Mentorship from senior developers
• Corporate training solutions for scaling teams
• Open source contribution opportunities

**Partnership Opportunities:**
• Feature our success stories and developer profiles
• Collaborate on content about developer career growth
• Sponsor our training programs for underserved communities
• Access to our network of trained developers for hiring

We'd love to discuss how Open Build can support {target.name}'s mission while helping more developers start their careers.

Would you be available for a brief 15-minute call next week to explore potential collaboration?

Best regards,
Open Build Team
team@open.build
https://open.build

P.S. We're also working on some exciting new initiatives in AI-powered developer education that might interest your audience."""
            },
            
            'startup': {
                'subject': f"Junior Developer Training Solutions for {target.name}",
                'message': f"""Hello {target.contact_name or 'there'},

I'm reaching out from Open Build, where we specialize in training junior developers and helping companies build strong development teams.

I noticed {target.name} is likely scaling your engineering team, and I wanted to share how we can help accelerate your junior developers' growth while reducing your training overhead.

**Our Training Programs Include:**
• Structured mentorship programs
• Real-world project experience
• Industry-standard tools and practices
• Soft skills development for team integration

**What Makes Us Different:**
• Partnership with Buildly Labs for real project experience
• Focus on practical skills over theoretical knowledge
• Ongoing support and community access
• Affordable rates for startups

**Results We've Achieved:**
• 90%+ job placement rate for our graduates
• Average 40% reduction in onboarding time for junior hires
• Strong retention rates due to comprehensive preparation

Would you be interested in a brief conversation about how Open Build can support {target.name}'s growth? I'd love to learn more about your current challenges and share how we might help.

Best regards,
Open Build Team
team@open.build
https://open.build

*Currently offering special rates for early-stage startups*"""
            },
            
            'influencer': {
                'subject': f"Collaboration Opportunity: Open Build x {target.name}",
                'message': f"""Hi {target.contact_name or 'there'},

I've been following your work in the developer community, and I'm impressed by your impact on helping developers grow their careers.

I'm reaching out from Open Build, a nonprofit focused on training junior developers and bridging the gap between education and industry-ready skills.

**Why I'm Reaching Out:**
Your audience would benefit from learning about our proven pathways from bootcamp/self-taught to professional developer roles.

**Collaboration Ideas:**
• Guest content about junior developer career paths
• Featuring success stories from our program graduates
• Co-hosting workshops on developer career growth
• Sponsorship opportunities for our community programs

**What We Bring:**
• Real success stories and data from our programs
• Access to our network of mentors and industry professionals
• Unique insights into the junior developer job market
• Partnership with Buildly Labs for practical experience

We're always looking for authentic ways to reach developers who could benefit from mentorship and structured career guidance.

Would you be open to a brief chat about potential collaboration? I'd love to learn more about your content strategy and see where there might be synergy.

Best regards,
Open Build Team
team@open.build
https://open.build

*P.S. Happy to provide exclusive insights or data for your content if there's a good fit*"""
            },
            
            'community': {
                'subject': f"Community Partnership: Open Build + {target.name}",
                'message': f"""Hello {target.contact_name or 'Community Team'},

I hope you're doing well! I'm reaching out from Open Build, a nonprofit organization dedicated to training junior developers and creating pathways into tech careers.

We've been impressed by {target.name}'s commitment to supporting the developer community, and I believe there's an opportunity for meaningful collaboration.

**Partnership Opportunities:**
• Hosting career development workshops for your members
• Providing mentorship opportunities through our network
• Offering special access to our training programs
• Cross-promotion of community events and initiatives

**What We Bring to the Partnership:**
• Experienced mentors from industry-leading companies
• Structured career development programs
• Job placement support and industry connections
• Workshop content on practical development skills

**Our Impact:**
• Trained 100+ junior developers with 90%+ placement rate
• Strong partnerships with companies looking to hire
• Focus on underrepresented communities in tech
• Sustainable, community-driven approach to education

We'd love to explore how Open Build can support {target.name}'s members while strengthening both our communities.

Would you be interested in a brief conversation about potential collaboration? I'm happy to work around your schedule.

Best regards,
Open Build Team
team@open.build
https://open.build

*Building stronger developer communities together*"""
            }
        }
        
        # Default template if category not found
        default_template = templates.get(category, templates['startup'])
        return default_template['subject'], default_template['message']

class EmailSender:
    """Handles email sending with Brevo SMTP integration"""
    
    def __init__(self, config: Dict):
        self.smtp_host = config['smtp_host']
        self.smtp_port = config['smtp_port']
        self.smtp_user = config['smtp_user']
        self.smtp_password = config['smtp_password']
        self.from_email = config['from_email']
        self.from_name = config['from_name']
        self.reply_to = config['reply_to']
    
    def send_email(self, to_email: str, subject: str, message: str, 
                   bcc_email: str = "team@open.build,greg@open.build") -> bool:
        """Send personalized outreach email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Bcc'] = bcc_email
            msg['Reply-To'] = self.reply_to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to Brevo SMTP
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            
            # Send email
            bcc_recipients = [email.strip() for email in bcc_email.split(',')]
            recipients = [to_email] + bcc_recipients
            text = msg.as_string()
            server.sendmail(self.from_email, recipients, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_daily_report(self, stats: Dict, targets_contacted: List[Target]):
        """Send daily report to team@open.build"""
        subject = f"Open Build Outreach Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
        
        message = f"""Daily Outreach Automation Report
================================

📊 Today's Statistics:
• New targets discovered: {stats.get('new_targets', 0)}
• Emails sent: {stats.get('emails_sent', 0)}
• Total targets in database: {stats.get('total_targets', 0)}

📋 Targets Contacted Today:
"""
        
        for target in targets_contacted:
            message += f"• {target.name} ({target.category}) - {target.email}\n"
        
        message += f"""

🎯 Pipeline Status:
• Targets awaiting response: {stats.get('awaiting_response', 0)}
• Targets ready for follow-up: {stats.get('ready_for_followup', 0)}

📈 Performance Metrics:
• Average response rate: {stats.get('response_rate', 0)}%
• Total organizations contacted: {stats.get('total_contacted', 0)}

---
Generated by Open Build Outreach Automation System
"""
        
        self.send_email("team@open.build", subject, message, "greg@open.build")

class OutreachAutomation:
    """Main automation system coordinator"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.db_manager = DatabaseManager()
        self.target_discovery = TargetDiscovery(self.db_manager)
        self.email_sender = EmailSender(self.config['email'])
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file and substitute environment variables"""
        default_config = {
            "email": {
                "smtp_host": os.getenv("BREVO_SMTP_HOST"),
                "smtp_port": int(os.getenv("BREVO_SMTP_PORT", "587")),
                "smtp_user": os.getenv("BREVO_SMTP_USER"),
                "smtp_password": os.getenv("BREVO_SMTP_PASSWORD"),
                "from_email": os.getenv("FROM_EMAIL"),
                "from_name": os.getenv("FROM_NAME"),
                "reply_to": os.getenv("REPLY_TO_EMAIL")
            },
            "limits": {
                "daily_emails": 20,
                "contacts_per_org": 4,
                "cooldown_days": 30
            },
            "discovery": {
                "targets_per_run": 10,
                "sources_per_category": 2
            }
        }
        
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                config_template = json.load(f)
            
            # Substitute environment variables in config
            config = self._substitute_env_vars(config_template)
            
            # Merge with defaults
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
        else:
            config = default_config
            # Create config template without sensitive values
            config_template = {
                "email": {
                    "smtp_host": "${BREVO_SMTP_HOST}",
                    "smtp_port": "${BREVO_SMTP_PORT}",
                    "smtp_user": "${BREVO_SMTP_USER}",
                    "smtp_password": "${BREVO_SMTP_PASSWORD}",
                    "from_email": "${FROM_EMAIL}",
                    "from_name": "${FROM_NAME}",
                    "reply_to": "${REPLY_TO_EMAIL}"
                },
                "limits": {
                    "daily_emails": 15,
                    "contacts_per_org": 4,
                    "cooldown_days": 30
                },
                "discovery": {
                    "targets_per_run": 10,
                    "sources_per_category": 2
                }
            }
            with open(config_path, 'w') as f:
                json.dump(config_template, f, indent=2)
            logger.info(f"Created config template file: {config_path}")
        
        # Validate required environment variables
        required_env_vars = [
            'BREVO_SMTP_HOST', 'BREVO_SMTP_USER', 'BREVO_SMTP_PASSWORD',
            'FROM_EMAIL', 'FROM_NAME', 'REPLY_TO_EMAIL'
        ]
        
        missing_vars = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return config
    
    def _substitute_env_vars(self, obj):
        """Recursively substitute environment variables in config"""
        if isinstance(obj, dict):
            return {key: self._substitute_env_vars(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
            env_var = obj[2:-1]
            return os.getenv(env_var, obj)
        else:
            return obj
    
    async def run_daily_automation(self):
        """Run the complete daily automation process"""
        logger.info("Starting daily outreach automation...")
        
        stats = {
            'new_targets': 0,
            'emails_sent': 0,
            'total_targets': 0,
            'errors': 0
        }
        
        targets_contacted = []
        
        try:
            # 1. Discover new targets
            logger.info("Phase 1: Discovering new targets...")
            new_targets = await self.target_discovery.discover_targets()
            
            for target in new_targets:
                if self.db_manager.add_target(target):
                    stats['new_targets'] += 1
                    logger.info(f"Added new target: {target.name}")
            
            # 2. Get targets ready for outreach
            logger.info("Phase 2: Preparing outreach list...")
            targets_for_outreach = self.db_manager.get_targets_for_outreach(
                limit=self.config['limits']['daily_emails']
            )
            
            # 3. Send outreach emails
            logger.info(f"Phase 3: Sending {len(targets_for_outreach)} outreach emails...")
            
            for target in targets_for_outreach:
                try:
                    # Get personalized message
                    subject, message = MessageTemplates.get_template(target.category, target)
                    
                    # Send email
                    success = self.email_sender.send_email(target.email, subject, message)
                    
                    if success:
                        # Update database
                        self.db_manager.update_contact_status(target.url)
                        targets_contacted.append(target)
                        stats['emails_sent'] += 1
                        
                        # Rate limiting between emails
                        await asyncio.sleep(random.uniform(60, 120))
                    else:
                        stats['errors'] += 1
                
                except Exception as e:
                    logger.error(f"Error processing target {target.name}: {e}")
                    stats['errors'] += 1
            
            # 4. Send daily report
            logger.info("Phase 4: Sending daily report...")
            self.email_sender.send_daily_report(stats, targets_contacted)
            
            logger.info(f"Daily automation completed successfully. "
                       f"New targets: {stats['new_targets']}, "
                       f"Emails sent: {stats['emails_sent']}")
        
        except Exception as e:
            logger.error(f"Error in daily automation: {e}")
            # Send error report
            error_subject = "Open Build Outreach Automation - Error Report"
            error_message = f"An error occurred during daily automation:\n\n{str(e)}\n\nPlease check the logs for more details."
            self.email_sender.send_email("team@open.build", error_subject, error_message)
    
    def generate_report(self) -> str:
        """Generate comprehensive outreach report"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        # Get summary statistics
        cursor.execute("SELECT COUNT(*) FROM targets")
        total_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM targets WHERE contact_count > 0")
        contacted_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM targets GROUP BY category")
        category_breakdown = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) FROM outreach_log WHERE created_at >= date('now', '-7 days')")
        emails_last_7_days = cursor.fetchone()[0]
        
        conn.close()
        
        report = f"""
🚀 Open Build Outreach Automation Report
========================================

📊 Overall Statistics:
• Total targets in database: {total_targets}
• Targets contacted: {contacted_targets}
• Emails sent (last 7 days): {emails_last_7_days}
• Contact rate: {(contacted_targets/total_targets*100):.1f}%

📋 Target Breakdown by Category:
"""
        
        for category, count in category_breakdown:
            report += f"• {category.title()}: {count}\n"
        
        report += f"""
📈 Performance Metrics:
• Average targets discovered per day: {total_targets / max(1, (datetime.now() - datetime(2024, 1, 1)).days)}
• Outreach efficiency: {(emails_last_7_days / 7):.1f} emails/day

---
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Open Build Outreach Automation System')
    parser.add_argument('--run', action='store_true', help='Run daily automation')
    parser.add_argument('--report', action='store_true', help='Generate and display report')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    
    args = parser.parse_args()
    
    if args.report:
        automation = OutreachAutomation(args.config)
        print(automation.generate_report())
    
    elif args.run:
        automation = OutreachAutomation(args.config)
        asyncio.run(automation.run_daily_automation())
    
    else:
        print("Open Build Outreach Automation System")
        print("Use --run to execute daily automation")
        print("Use --report to generate status report")

if __name__ == "__main__":
    main()
