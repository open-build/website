# Getting Started Guide Prompt - Day 2 Article

## Article Generation Instructions for Getting Started Guide

**Article Title:** "Getting Started: From Patient Data Concept to Production-Ready System"

**Category:** Implementation

**Day Number:** 2

**Link to Previous:** This article builds directly on Day 1's "Patient Data Management System" use case, showing readers how to move from concept to implementation.

---

## Content Structure Requirements

### 1. Opening Hook (100-150 words)
- Reference Emily from Day 1's Patient Data Management System article
- Transition from understanding the problem to taking action
- Preview what product managers and developers will accomplish by following this guide

### 2. Product Manager Getting Started Section (300-400 words)

**Subsection: Understanding the Radical Therapy Process**
- Link to https://radicaltherapy.dev and explain the methodology
- Show how it applies specifically to healthcare data management
- Reference the 5-phase approach from Day 1

**Subsection: Hands-On with Buildly Labs**
- Direct readers to https://labs.buildly.io
- Explain how to access the Patient Data Management lab
- Walk through the interactive tutorial for Emily's use case
- Show how PMs can prototype without writing code

**Subsection: Planning with AI Assistance**
- Reference how Copilot can help with requirement gathering
- Show prompts for generating user stories and acceptance criteria
- Link to https://docs.buildly.io for comprehensive documentation

### 3. Developer Getting Started Section (400-500 words)

**Subsection: Setting Up Your Development Environment**
- Install buildly-cli: `npm install -g @buildly/cli`
- Initialize project: `buildly create patient-data-system`
- Reference https://docs.buildly.io/cli/getting-started

**Subsection: Backend Development with Buildly CLI**
- Generate microservice structure for patient data
- Show actual CLI commands:
  - `buildly generate service patient-service`
  - `buildly add model Patient`
  - `buildly add endpoint patients`
- Explain how this relates to Emily's security requirements

**Subsection: Frontend Development with React Template**
- Use Buildly's React template: `buildly create-frontend react`
- Show component structure for patient dashboard
- Integrate with backend APIs automatically generated

**Subsection: AI-Powered Development with Copilot**
- Show specific prompts for healthcare compliance code
- Demonstrate HIPAA-compliant data handling patterns
- Use Copilot to generate security validation code

### 4. Integration and Deployment (200-300 words)
- Connect frontend and backend using Buildly's orchestration
- Show how to deploy to cloud using Buildly's deployment tools
- Reference production considerations from https://docs.buildly.io

### 5. Next Steps and Tomorrow's Preview (150-200 words)
- What readers accomplished: working prototype of Emily's system
- Preview Day 3: "Advanced Security Patterns for Healthcare Data"
- Encourage readers to share their progress

---

## Required Source References

**Must Include These URLs:**
- https://labs.buildly.io (interactive learning platform)
- https://radicaltherapy.dev (development process methodology)
- https://docs.buildly.io (comprehensive documentation)
- https://github.com/buildlyio (open source tools and templates)
- https://www.buildly.io (main platform overview)

**Link to Previous Content:**
- Reference "Day 1: Patient Data Management System" article
- Build continuity by mentioning Emily's specific challenges
- Show how today's tools solve yesterday's problems

---

## Code Examples Required

### Product Manager Section:
- Copilot prompts for generating user stories
- Examples of requirement gathering with AI assistance

### Developer Section:
- Complete buildly-cli command sequence
- React component code for patient dashboard
- Security validation code generated with Copilot
- Integration configuration examples

---

## Learning Outcomes

**Product Managers Will Learn:**
- How to use labs.buildly.io for rapid prototyping
- Applying Radical Therapy methodology to healthcare projects
- Leveraging AI for requirement specification and validation

**Developers Will Learn:**
- Setting up cloud-native development environment with buildly-cli
- Creating secure, compliant backend services
- Building responsive React frontends with Buildly templates
- Using Copilot effectively for healthcare compliance code

---

## Quality Criteria

1. **Practical Focus:** Every section must include actionable steps
2. **Continuity:** Clear connections to Day 1's Patient Data Management case
3. **Comprehensive Coverage:** Both PM and developer perspectives addressed
4. **Source Integration:** Natural integration of all required URLs and documentation
5. **AI Emphasis:** Show how AI assistance accelerates both planning and development
6. **Compliance Awareness:** Healthcare-specific considerations throughout

---

## Word Count Target: 1200-1500 words

## Tone: Professional, instructional, encouraging - helping readers move from concept to working prototype

**Generate this article following the Radical Therapy methodology, emphasizing speed AND quality through AI assistance, and ensuring all referenced tools and processes are properly explained and linked.**