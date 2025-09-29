# Open Build Training Blog - Article Generation Prompts

## Master Prompt Template

This document contains the evolving prompt system for generating daily technical training articles. The AI system learns and improves with each article generated.

### Core Mission Statement
Generate comprehensive technical training articles that teach developers and product managers how to build cloud native services using AI assistance, focusing on removing boring repetitive work so they can focus on creative challenges.

### Article Structure Framework

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

*This prompt document evolves continuously based on article performance and reader feedback. Last updated: 2025-09-29*