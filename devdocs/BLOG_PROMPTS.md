# Open Build Training Blog - Article Generation Prompts

## Master Prompt Template

This document contains the evolving prompt system for generating daily technical training articles. The AI system learns and improves with each article generated.

### Core Mission Statement
Generate comprehensive technical training articles that teach developers and product managers how to build cloud native services using AI assistance, focusing on removing boring repetitive work so they can focus on creative challenges.

### Required Source References
Every article MUST reference and integrate content from these authoritative sources:

1. **Buildly.io Platform**: https://www.buildly.io
2. **Buildly.io Documentation**: https://docs.buildly.io
3. **Radical Therapy Process**: https://radicaltherapy.dev
4. **Open Source Tools**: https://github.com/buildlyio
5. **Buildly Labs Platform**: https://labs.buildly.io

### Complete Article Generation Prompt

Use this comprehensive prompt for each article generation:

### Complete Daily Article Generation Prompt

```
# COMPREHENSIVE TRAINING BLOG ARTICLE GENERATION

## CONTEXT AND MISSION
You are writing a technical training article for the Open Build foundry training blog that teaches developers and product managers how to build cloud native services using AI assistance. The core principle is to show how AI removes boring, repetitive work so professionals can focus on creative challenges and unique business logic.

## ARTICLE REQUIREMENTS

### Article Details:
- **Day Number**: {day_number}
- **Industry**: {category}
- **Business Title**: {title}
- **Business Problem**: {business_problem}
- **Technical Focus**: {technical_focus}
- **AI Assistance Areas**: {ai_assistance}

### Target Audience:
- **Developers**: Learn AI-assisted development techniques
- **Product Managers**: Understand how AI accelerates delivery and improves quality
- **Both**: Focus on creative challenges rather than boilerplate code

### Required Source Integration:
You MUST reference and integrate practical examples from these VERIFIED sources:
- **Buildly.io Platform**: https://www.buildly.io (main platform)
- **Buildly.io Documentation**: https://docs.buildly.io (technical documentation - VERIFIED)
- **Buildly CLI Repository**: https://github.com/buildlyio/buildly-cli (actual CLI commands - VERIFIED)
- **Radical Therapy Process**: https://radicaltherapy.dev (development methodology)

### CRITICAL: Use Only Real Technical Information
Before writing any technical content, consult the BUILDLY_REAL_DOCS.md reference file which contains VERIFIED information about:
- Actual CLI commands and workflow (not fabricated ones)
- Real Product Labs features and capabilities
- True BabbleBeaver AI integration process
- Documented architecture and infrastructure
- **Open Source Tools**: https://github.com/buildlyio (community tools)
- **Buildly Labs Platform**: https://labs.buildly.io (deployment platform)

## ARTICLE STRUCTURE (FOLLOW EXACTLY)

### 1. Business Use Case Introduction (200-300 words)
Create a compelling narrative featuring a fictional professional facing the exact business challenge:

**Requirements:**
- Start with "Meet [Name], a [role] at [company type]..."
- Include concrete numbers (costs, time wasted, scale)
- Show why traditional approaches fail
- Demonstrate business impact and urgency
- Set up cloud native + AI as the solution

**Example Opening:**
"Meet Sarah, a VP of Engineering at a growing e-commerce company processing 50,000 orders daily. Her team spends 60% of their time on repetitive infrastructure tasks instead of building features that drive revenue..."

### 2. Buildly.io Platform Integration (400-500 words)
Demonstrate practical usage of Buildly.io tools with working examples:

**Required Tools to Feature:**
- **Buildly Core**: Microservice orchestration (reference https://docs.buildly.io/core/)
- **Buildly Marketplace**: Pre-built components
- **Buildly CLI**: Development tools and automation
- **API Gateway**: Configuration and routing
- **Service Mesh**: Integration patterns

**Include:**
- Actual configuration files (YAML, JSON)
- CLI commands with expected output
- Code snippets showing integration
- Architecture diagrams (described in text)
- Step-by-step implementation guide

**Example:**
```yaml
# buildly-core-config.yaml
services:
  catalog:
    image: "catalog-service:latest"
    environment:
      DATABASE_URL: "${DATABASE_URL}"
    ports:
      - "8001:8000"
```

### 3. Radical Therapy Development Process (300-400 words)
Follow the exact methodology from https://radicaltherapy.dev:

**Process Steps (follow exactly):**
1. **Problem Analysis**: Understanding business context and requirements
2. **AI-Assisted Design**: Generate architecture and patterns with AI
3. **Rapid Prototyping**: Build MVP using AI tools and templates
4. **Iterative Enhancement**: Learn from feedback and improve
5. **Production Deployment**: Scale and monitor with AI assistance

**For each step, show:**
- What humans do (strategic thinking, creativity, business decisions)
- What AI handles (code generation, boilerplate, patterns, testing)
- How they collaborate for optimal results
- Specific tools and techniques used
- Measurable outcomes (time saved, quality improved)

**Emphasize**: Speed AND quality, not speed OR quality

### 4. AI-Assisted Implementation (500-600 words)
Provide detailed, practical AI assistance examples:

**Structure:**
- **The Boring Work AI Handles**: 
  - Boilerplate code generation
  - Test case creation
  - Configuration file generation
  - Documentation writing
  - Error handling patterns

- **Creative Work Humans Focus On**:
  - Business logic design
  - User experience decisions
  - Architecture choices
  - Performance optimization strategies
  - Security considerations

- **Practical AI Prompts** (Include 2-3 working examples):
```
Prompt: "Generate a microservice API endpoint for product catalog with pagination, filtering, and error handling using FastAPI"

Expected Output: [Show actual code]
```

- **Quality Assurance**: How AI helps with testing, code review, and compliance

### 5. Open Source Integration (200-300 words)
Highlight tools from https://github.com/buildlyio:

**Focus Areas:**
- Community-contributed components and extensions
- Integration examples and templates
- How to contribute and collaborate
- Pre-built solutions that accelerate development
- Community support and documentation

**Show practical examples:**
- Installing and using open source components
- Contributing improvements back to the community
- Leveraging community solutions for faster development

### 6. Buildly Labs Platform Usage (200-300 words)
Demonstrate https://labs.buildly.io deployment and operations:

**Cover:**
- **Deployment**: One-click deployment from development to production
- **Scaling**: Auto-scaling configuration and monitoring
- **DevOps**: CI/CD pipeline setup and automation
- **Monitoring**: Performance analytics and alerting
- **Collaboration**: Team workflows and environments

**Include practical examples:**
- Deployment commands and configurations
- Monitoring dashboard setup
- Performance optimization techniques

### 7. Key Takeaways & Next Steps (150-200 words)
Summarize concrete learning outcomes:

**For Developers:**
- Specific AI tools and techniques learned today
- Time savings compared to traditional approaches
- Code quality improvements achieved
- New skills acquired

**For Product Managers:**
- Faster delivery timelines enabled
- Reduced development costs and risks
- Improved predictability and quality
- Better team productivity

**Next Article Preview:**
- Tomorrow's related topic and industry focus
- How it builds on today's learning
- Continuing the journey of AI-assisted development

## TECHNICAL REQUIREMENTS

### Code Quality:
- All code examples must be working and tested
- Include proper error handling and logging
- Show both development and production configurations
- Provide complete file paths and directory structures

### References:
- Link to actual documentation pages
- Reference specific GitHub repositories
- Include version numbers where applicable
- Provide working URLs for all external resources

### Tone and Style:
- Professional but approachable and conversational
- Use "we" and "let's" to create partnership feeling
- Focus on practical value over theoretical concepts
- Show, don't just tell - include working examples
- Inspire confidence and creativity

### Word Count Targets:
- Total article: 2000-2500 words
- Each section must meet specified word counts
- Balance depth with readability
- Include subheadings for easy scanning

## LEARNING AND IMPROVEMENT

### Success Metrics:
- Technical accuracy and working code examples
- Practical implementability by readers
- Clear value proposition for both audiences
- Proper integration of all required sources
- Engaging and inspiring tone

### Continuous Improvement:
- Each article should build on previous learnings
- Incorporate feedback and performance data
- Evolve examples based on real-world usage
- Stay current with tool updates and best practices

Generate a complete article following this structure exactly, ensuring all requirements are met and all sources are properly referenced with working examples.
```

### Article Structure Framework (Detailed Breakdown)

#### 1. Business Use Case Introduction (200-300 words)
**Prompt Section:**
```
Create a compelling business scenario introduction that:
- Presents a real-world business problem that needs solving
- Explains why traditional approaches fall short
- Shows the business impact of the problem (costs, inefficiencies, missed opportunities)
- Sets up the cloud native solution as the answer

Business Context: {business_context}
Industry: {industry}
Problem Statement: {problem_statement}

Write this as a story featuring a fictional professional facing this exact challenge.
```

**Quality Criteria:**
- Uses concrete numbers and scenarios
- Relatable to both technical and business audiences
- Creates urgency and demonstrates value

#### 2. Buildly.io Tools Integration (400-500 words)
**Prompt Section:**
```
Demonstrate practical usage of Buildly.io platform tools:

Required Tools to Feature:
- Buildly Core: Microservice orchestration platform
- Buildly Marketplace: Pre-built service components
- Buildly CLI: Command line development tools
- Service mesh integration capabilities

Show concrete code examples and configuration snippets.
Reference: https://www.buildly.io

Integration Patterns to Highlight:
- {integration_pattern}
- API Gateway configuration
- Service discovery and registration
- Container deployment automation

Provide step-by-step implementation guidance with actual commands.
```

**Quality Criteria:**
- Includes working code examples
- Shows real configuration files
- Demonstrates practical value
- Links to actual Buildly.io resources

#### 3. Radical Therapy Development Process (300-400 words)
**Prompt Section:**
```
Follow the Radical Therapy development methodology:

Process Steps (follow exactly):
1. Problem Analysis - Understanding business context and requirements
2. AI-Assisted Design - Generate architecture and patterns with AI
3. Rapid Prototyping - Build MVP using AI tools and templates
4. Iterative Enhancement - Learn from feedback and improve
5. Production Deployment - Scale and monitor with AI assistance

For each step, show:
- What the human does (creative, strategic thinking)
- What AI handles (code generation, boilerplate, patterns)
- How they work together for optimal results

Reference: https://radicaltherapy.dev
Emphasize speed AND quality, not speed OR quality.
```

**Quality Criteria:**
- Clear separation of human vs AI tasks
- Practical implementation steps
- Focuses on learning and improvement
- Shows measurable outcomes

#### 4. AI-Assisted Implementation (500-600 words)
**Prompt Section:**
```
Provide detailed AI assistance examples for: {ai_assistance_focus}

Structure:
- **The Boring Work AI Handles:**
  - Specific code generation examples
  - Boilerplate template creation
  - Pattern implementation
  - Testing and validation scripts

- **Creative Work Humans Focus On:**
  - Business logic design
  - User experience decisions
  - Architecture choices
  - Problem-solving strategies

- **Practical AI Prompts:**
  Include 2-3 actual AI prompts that generate useful code
  Show the input prompt and expected output

- **Quality Assurance:**
  How AI helps with testing, code review, and compliance
```

**Quality Criteria:**
- Real, working AI prompts
- Demonstrable code examples
- Clear value proposition
- Measurable time savings

#### 5. Open Source Integration (200-300 words)
**Prompt Section:**
```
Highlight relevant open source tools from GitHub:

Repository: https://github.com/buildlyio
Focus areas:
- Community-contributed components
- Extensions and plugins
- Integration examples
- Contribution opportunities

Show how open source accelerates development:
- Pre-built solutions
- Community support
- Collaborative improvement
- Reduced time-to-market
```

#### 6. Buildly Labs Platform Usage (200-300 words)
**Prompt Section:**
```
Demonstrate https://labs.buildly.io platform features:

Deployment & Scaling:
- One-click deployment options
- Auto-scaling configuration
- Performance monitoring
- DevOps automation

Show practical examples of:
- Deploying the solution built in the article
- Monitoring and analytics setup
- CI/CD pipeline configuration
```

#### 7. Key Takeaways & Next Steps (150-200 words)
**Prompt Section:**
```
Summarize learning outcomes:

For Developers:
- Specific AI tools and techniques learned
- Time saved vs traditional approaches
- Quality improvements achieved

For Product Managers:
- Faster delivery timelines
- Reduced development costs
- Improved predictability

Next Article Preview:
- Related topic for tomorrow
- How it builds on today's learning
```

### Learning and Improvement System

#### Article Performance Metrics
Track these metrics for each article to improve future prompts:

1. **Technical Accuracy**: Code examples work correctly
2. **Practical Value**: Readers can implement the solution  
3. **Clarity**: Complex concepts explained simply
4. **Completeness**: All required sections covered adequately
5. **Engagement**: Compelling and interesting to read

#### Prompt Evolution Rules

1. **Successful Patterns**: If an article generates positive feedback, add the prompt patterns to the "Proven Effective" section below
2. **Failed Approaches**: Document what doesn't work to avoid repeating
3. **Reader Feedback**: Incorporate specific suggestions into future prompts
4. **Technical Updates**: Keep code examples current with latest tool versions

### Proven Effective Prompt Patterns

#### For Business Use Cases:
- "Meet [Name], a [role] at a [type] company facing [specific challenge]..."
- Include concrete numbers: "$X cost per month", "Y hours wasted daily"
- Show before/after scenarios clearly

#### For Technical Content:
- Start with "Let's build..." rather than "You could build..."
- Include actual file names and directory structures
- Provide copy-pasteable code blocks
- Show expected output/results

#### For AI Integration:
- Format AI prompts in clear code blocks
- Show the exact input and expected output
- Explain why the prompt works
- Provide variations for different scenarios

### Category-Specific Enhancements

#### E-commerce Articles:
- Focus on scalability and performance
- Include payment processing considerations
- Address security and compliance
- Show inventory management patterns

#### Healthcare Articles:
- Emphasize HIPAA compliance throughout
- Include audit trail requirements
- Show data encryption examples
- Address patient privacy concerns

#### FinTech Articles:
- Highlight security and fraud prevention
- Include regulatory compliance
- Show transaction processing patterns
- Address data consistency requirements

#### Education Articles:
- Focus on user experience and accessibility
- Include analytics and progress tracking
- Show content delivery optimization
- Address scalability for large user bases

#### IoT Articles:
- Emphasize real-time data processing
- Include device management patterns
- Show time series data handling
- Address edge computing considerations

### Quality Checklist

Before publishing each article, ensure:

- [ ] All code examples are tested and work
- [ ] Links to Buildly.io and RadicalTherapy.dev are included
- [ ] Business value is clearly articulated
- [ ] AI assistance examples are practical and specific
- [ ] Article follows the exact structure outlined above
- [ ] Next day's topic is teased appropriately
- [ ] Word count targets are met for each section
- [ ] Technical terms are explained for mixed audiences

### Feedback Integration Process

1. **Daily Review**: Assess each article's clarity and completeness
2. **Weekly Analysis**: Look for patterns in successful vs unsuccessful content
3. **Monthly Updates**: Update this prompt document with proven patterns
4. **Quarterly Overhaul**: Major updates to structure or approach based on accumulated learning

---

## Day 2 Implementation Article - Getting Started Guide

### Specialized Prompt for Implementation Articles

**Article Type:** Getting Started Implementation Guide  
**Purpose:** Bridge the gap from concept (Day 1) to working system  
**Target:** Both Product Managers and Developers taking action  

### Key Components Required:
1. **Product Manager Section:**
   - Interactive learning with https://labs.buildly.io
   - Practical application of https://radicaltherapy.dev methodology
   - AI-assisted requirement gathering and planning

2. **Developer Section:**
   - Environment setup with buildly-cli commands
   - Backend service generation with security patterns
   - React frontend templates with healthcare UI components
   - Copilot integration for compliance code generation

3. **Integration & Deployment:**
   - Service orchestration configuration
   - Compliance validation and audit logging
   - Production deployment considerations

### Required Resource Integration:
- **Interactive Labs:** https://labs.buildly.io for hands-on learning
- **Technical Documentation:** https://docs.buildly.io for API references
- **Development Process:** https://radicaltherapy.dev for methodology
- **Open Source Tools:** https://github.com/buildlyio for templates and examples

### Continuity Requirements:
- Direct reference to previous day's use case (Emily's Patient Data Management)
- Show progression from problem understanding to working solution
- Maintain consistent tone and technical depth
- Preview next day's advanced topics

### Code Example Requirements:
- Complete CLI command sequences that readers can copy/paste
- Copilot prompts with expected outputs
- Integration configuration examples
- Security validation patterns specific to use case

---

*This prompt document evolves continuously based on article performance and reader feedback. Last updated: 2025-09-29*