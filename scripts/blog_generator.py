#!/usr/bin/env python3
"""
Op        # Configuration from environment
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://pop-os2.local:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
        self.blog_enabled = os.getenv("BLOG_ENABLED", "true").lower() == "true"Build Training Blog Article Generator
Connects to Ollama service to generate daily technical articles
"""

import os
import json
import requests
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional
import hashlib

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/blog_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BlogArticleGenerator:
    def __init__(self):
        # Configuration from environment
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://pop-os2.local:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
        self.blog_enabled = os.getenv("BLOG_ENABLED", "true").lower() == "true"
        
        # Blog settings
        self.articles_dir = Path("blog/articles")
        self.articles_dir.mkdir(parents=True, exist_ok=True)
        
        # Database for tracking articles and learning
        self.db_path = "blog_articles.db"
        self.init_database()
        
        # Load reference content
        self.load_reference_content()
        
        # Article categories and business use cases
        self.business_use_cases = [
            {
                "category": "E-commerce",
                "title": "Building a Product Catalog Microservice",
                "business_problem": "Managing thousands of products with real-time inventory",
                "technical_focus": "Microservices, API Gateway, Database Design",
                "ai_assistance": "Code generation, API endpoint creation, database schema optimization"
            },
            {
                "category": "Healthcare",
                "title": "Patient Data Management System",
                "business_problem": "Secure, compliant patient record management with HIPAA compliance",
                "technical_focus": "Security, Encryption, Audit Trails",
                "ai_assistance": "Security pattern implementation, compliance checking, audit log generation"
            },
            {
                "category": "FinTech",
                "title": "Real-time Payment Processing Service",
                "business_problem": "Processing thousands of transactions per second with fraud detection",
                "technical_focus": "Event Streaming, Async Processing, Monitoring",
                "ai_assistance": "Event handler generation, monitoring setup, performance optimization"
            },
            {
                "category": "Education",
                "title": "Learning Management Platform",
                "business_problem": "Scalable course delivery with progress tracking and analytics",
                "technical_focus": "Video Streaming, Analytics, User Management",
                "ai_assistance": "Analytics dashboard creation, user flow optimization, content delivery setup"
            },
            {
                "category": "IoT",
                "title": "Smart Building Management System",
                "business_problem": "Real-time monitoring and control of building systems and energy usage",
                "technical_focus": "Time Series Data, Real-time Analytics, Device Management",
                "ai_assistance": "Data pipeline creation, real-time processing logic, alert system setup"
            }
        ]

    def init_database(self):
        """Initialize SQLite database for article tracking and learning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                business_use_case TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                performance_score REAL DEFAULT 0,
                feedback_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                published BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Learning feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS article_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                feedback_type TEXT,
                feedback_data TEXT,
                created_at TEXT,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        """)
        
        # Generation prompts evolution table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt_evolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_version TEXT NOT NULL,
                prompt_content TEXT NOT NULL,
                performance_metrics TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")

    def load_reference_content(self):
        """Load reference content from buildly.io and radicaltherapy.dev"""
        # This would ideally fetch from the actual sites
        # For now, we'll use predefined reference content
        
        self.buildly_reference = {
            "core_concepts": [
                "Microservice orchestration with Buildly Core",
                "API Gateway configuration and routing",
                "Service mesh integration",
                "Container deployment strategies",
                "Data pipeline automation"
            ],
            "tools": [
                "Buildly Core - Microservice orchestration platform",
                "Buildly UI - Frontend component library", 
                "Buildly CLI - Command line development tools",
                "Buildly Marketplace - Pre-built service components"
            ],
            "patterns": [
                "Event-driven architecture",
                "CQRS (Command Query Responsibility Segregation)",
                "Saga pattern for distributed transactions",
                "Circuit breaker pattern for resilience",
                "API versioning strategies"
            ]
        }
        
        self.radical_therapy_reference = {
            "principles": [
                "Rapid prototyping with AI assistance",
                "Test-driven development with AI-generated tests",
                "Continuous learning and adaptation",
                "Focus on business value over technical complexity",
                "Collaborative AI-human development workflows"
            ],
            "process_steps": [
                "1. Problem Analysis - Understanding business context",
                "2. AI-Assisted Design - Generate architecture with AI",
                "3. Rapid Prototyping - Build MVP with AI tools",
                "4. Iterative Enhancement - Learn and improve",
                "5. Production Deployment - Scale and monitor"
            ],
            "ai_integration": [
                "Code generation for boilerplate and patterns",
                "Test case generation and validation",
                "Documentation and API spec creation", 
                "Performance optimization suggestions",
                "Security review and compliance checking"
            ]
        }

    def generate_article_prompt(self, use_case: Dict, day_number: int) -> str:
        """Generate comprehensive prompt for article creation"""
        
        base_prompt = f"""
# TRAINING BLOG ARTICLE GENERATION PROMPT

## MISSION
Write a comprehensive technical training article (Day {day_number}) that teaches developers and product managers how to build cloud native services using AI assistance, focusing on removing boring repetitive work so they can focus on creative challenges.

## ARTICLE REQUIREMENTS

### Business Context
- **Industry:** {use_case['category']}
- **Title:** {use_case['title']}
- **Business Problem:** {use_case['business_problem']}
- **Technical Focus:** {use_case['technical_focus']}

### Learning Objectives
1. **For Developers:** Learn to use AI for {use_case['ai_assistance']}
2. **For Product Managers:** Understand how AI accelerates delivery and improves quality
3. **For Both:** Focus on unique business logic rather than boilerplate code

### Required Content Structure

#### 1. Business Use Case Introduction (200-300 words)
- Real-world scenario and business impact
- Why traditional approaches fall short
- How modern cloud native architecture solves this

#### 2. Buildly.io Tools Integration (400-500 words)
Reference these specific tools and show practical usage:
- **Buildly Core:** {self.buildly_reference['core_concepts'][0]}
- **Service Components:** Pre-built modules from Buildly Marketplace
- **Integration Patterns:** {self.buildly_reference['patterns'][0]}

Show concrete code examples with these tools.

#### 3. Radical Therapy Development Process (300-400 words)
Follow this process structure:
{chr(10).join(self.radical_therapy_reference['process_steps'])}

Emphasize AI assistance at each step.

#### 4. AI-Assisted Implementation (500-600 words)
- **What AI Handles:** {use_case['ai_assistance']}
- **What Humans Focus On:** Unique business logic and creative problem-solving
- **Practical Examples:** Show actual AI prompts and generated code
- **Quality Assurance:** How AI helps with testing and validation

#### 5. Open Source Integration (200-300 words)
- Relevant tools from https://github.com/buildlyio
- Community contributions and extensions
- How open source accelerates development

#### 6. Buildly Labs Platform Usage (200-300 words)  
- https://labs.buildly.io deployment and scaling
- Monitoring and analytics features
- DevOps automation capabilities

#### 7. Key Takeaways & Next Steps (150-200 words)
- What developers learned about AI-assisted development
- What product managers learned about accelerated delivery
- Tomorrow's related topic preview

### Technical Requirements
- Include 2-3 code examples with AI generation prompts
- Add practical implementation tips
- Reference actual URLs: https://www.buildly.io, https://radicaltherapy.dev
- Use clear, actionable language
- Target 2000-2500 words total

### Tone and Style
- Professional but approachable
- Focus on practical value over theory  
- Emphasize speed AND quality
- Show how AI removes boring work
- Inspire creativity and innovation

Generate a complete article following this structure exactly.
"""
        return base_prompt

    def call_ollama(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Make request to Ollama service with retries"""
        
        # Try both API endpoints (newer and older versions)
        api_endpoints = ["/api/generate", "/v1/generate", "/generate"]
        
        for endpoint in api_endpoints:
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 3000
                }
            }
            
            for attempt in range(max_retries):
                try:
                    logger.info(f"Calling Ollama {endpoint} (attempt {attempt + 1}/{max_retries})")
                    response = requests.post(
                        f"{self.ollama_host}{endpoint}",
                        json=payload,
                        timeout=180
                    )
                    
                    if response.status_code == 404:
                        logger.info(f"Endpoint {endpoint} not found, trying next...")
                        break
                    
                    response.raise_for_status()
                    
                    result = response.json()
                    if 'response' in result:
                        logger.info("Article generated successfully")
                        return result['response']
                    else:
                        logger.error(f"Unexpected response format: {result}")
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Ollama request failed (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        logger.info("Retrying in 10 seconds...")
                        import time
                        time.sleep(10)
        
        logger.error("Failed to generate article after all retries and endpoints")
        return None

    def generate_daily_article(self) -> Optional[Dict]:
        """Generate today's article"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check if article already exists for today
        if self.article_exists(today):
            logger.info(f"Article already exists for {today}")
            return self.get_existing_article(today)
        
        # Determine day number and use case
        day_number = self.get_day_number()
        use_case = self.business_use_cases[day_number % len(self.business_use_cases)]
        
        logger.info(f"Generating Day {day_number} article: {use_case['title']}")
        
        # Generate article prompt
        prompt = self.generate_article_prompt(use_case, day_number)
        
        # Call Ollama to generate content
        content = self.call_ollama(prompt)
        
        if not content:
            logger.error("Failed to generate article content")
            return None
        
        # Save article to database
        article_data = {
            'date': today,
            'title': use_case['title'],
            'category': use_case['category'],
            'business_use_case': use_case['business_problem'],
            'content': content,
            'day_number': day_number
        }
        
        article_id = self.save_article(article_data)
        article_data['id'] = article_id
        
        # Save to file system
        self.save_article_file(article_data)
        
        logger.info(f"Article generated and saved: Day {day_number} - {use_case['title']}")
        return article_data

    def article_exists(self, date: str) -> bool:
        """Check if article exists for given date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM articles WHERE date = ?", (date,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    def get_existing_article(self, date: str) -> Dict:
        """Get existing article for date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, category, business_use_case, content_hash 
            FROM articles WHERE date = ?
        """, (date,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'date': date,
                'title': row[1],
                'category': row[2],
                'business_use_case': row[3]
            }
        return None

    def get_day_number(self) -> int:
        """Calculate day number since blog started"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM articles")
        count = cursor.fetchone()[0]
        conn.close()
        return count + 1

    def save_article(self, article_data: Dict) -> int:
        """Save article to database"""
        content_hash = hashlib.sha256(article_data['content'].encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO articles (date, title, category, business_use_case, content_hash, created_at, published)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            article_data['date'],
            article_data['title'],
            article_data['category'],
            article_data['business_use_case'],
            content_hash,
            datetime.now().isoformat(),
            True
        ))
        
        article_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return article_id

    def save_article_file(self, article_data: Dict):
        """Save article as HTML file"""
        # Create article HTML
        html_content = self.create_article_html(article_data)
        
        # Save to file
        filename = f"day-{article_data['day_number']}-{article_data['date']}.html"
        filepath = self.articles_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Article saved to {filepath}")

    def create_article_html(self, article_data: Dict) -> str:
        """Create HTML format for article"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']} - Open Build Training</title>
    <link rel="stylesheet" href="../assets/css/tailwind.css">
    <link rel="stylesheet" href="../assets/css/main.css">
</head>
<body class="bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 py-8">
        <nav class="mb-8">
            <a href="../training-blog.html" class="text-blue-600 hover:text-blue-800">&larr; Back to Training Blog</a>
        </nav>
        
        <article class="bg-white rounded-lg shadow-md p-8">
            <header class="mb-8">
                <div class="text-sm text-blue-600 font-medium mb-2">
                    DAY {article_data['day_number']} • {article_data['category'].upper()}
                </div>
                <h1 class="text-3xl font-bold text-gray-900 mb-4">{article_data['title']}</h1>
                <div class="text-gray-600">
                    <time datetime="{article_data['date']}">{datetime.strptime(article_data['date'], '%Y-%m-%d').strftime('%B %d, %Y')}</time>
                </div>
            </header>
            
            <div class="prose prose-lg max-w-none">
                {self.format_article_content(article_data['content'])}
            </div>
            
            <footer class="mt-12 pt-8 border-t border-gray-200">
                <div class="flex items-center justify-between">
                    <div class="text-sm text-gray-500">
                        <p>Generated with AI assistance using Ollama</p>
                        <p>Part of the Open Build daily training series</p>
                    </div>
                    <div class="space-x-4">
                        <a href="https://www.buildly.io" target="_blank" class="text-blue-600 hover:text-blue-800">Buildly.io</a>
                        <a href="https://radicaltherapy.dev" target="_blank" class="text-blue-600 hover:text-blue-800">Radical Therapy</a>
                        <a href="https://labs.buildly.io" target="_blank" class="text-blue-600 hover:text-blue-800">Buildly Labs</a>
                    </div>
                </div>
            </footer>
        </article>
    </div>
</body>
</html>"""

    def format_article_content(self, content: str) -> str:
        """Format AI-generated content for HTML display"""
        # Basic markdown-like formatting
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('<br>')
            elif line.startswith('# '):
                formatted_lines.append(f'<h2 class="text-2xl font-bold mt-8 mb-4">{line[2:]}</h2>')
            elif line.startswith('## '):
                formatted_lines.append(f'<h3 class="text-xl font-semibold mt-6 mb-3">{line[3:]}</h3>')
            elif line.startswith('- '):
                formatted_lines.append(f'<li class="mb-2">{line[2:]}</li>')
            elif line.startswith('```'):
                formatted_lines.append('<pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto"><code>')
            else:
                formatted_lines.append(f'<p class="mb-4">{line}</p>')
        
        return '\n'.join(formatted_lines)

    def get_recent_articles(self, limit: int = 5) -> List[Dict]:
        """Get recent articles for email inclusion"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date, title, category, business_use_case 
            FROM articles 
            ORDER BY date DESC 
            LIMIT ?
        """, (limit,))
        
        articles = []
        for row in cursor.fetchall():
            articles.append({
                'date': row[0],
                'title': row[1],
                'category': row[2],
                'business_use_case': row[3]
            })
        
        conn.close()
        return articles

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate training blog articles")
    parser.add_argument("--generate", action="store_true", help="Generate today's article")
    parser.add_argument("--test-ollama", action="store_true", help="Test Ollama connection")
    
    args = parser.parse_args()
    
    generator = BlogArticleGenerator()
    
    if args.test_ollama:
        logger.info("Testing Ollama connection...")
        test_response = generator.call_ollama("Hello, this is a test. Please respond with 'Connection successful!'")
        if test_response:
            logger.info(f"Ollama test successful: {test_response}")
        else:
            logger.error("Ollama test failed")
    
    elif args.generate:
        logger.info("Starting daily article generation...")
        article = generator.generate_daily_article()
        if article:
            logger.info(f"Successfully generated article: {article['title']}")
        else:
            logger.error("Failed to generate article")
    
    else:
        print("Open Build Training Blog Article Generator")
        print("Use --generate to create today's article")
        print("Use --test-ollama to test connection")