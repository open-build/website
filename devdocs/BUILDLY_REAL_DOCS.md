# REAL BUILDLY DOCUMENTATION REFERENCE

## Actual Buildly CLI Information

**Source:** https://github.com/buildlyio/buildly-cli

### Key Facts About Buildly CLI:
- **Purpose:** Comprehensive open source toolkit for AI-powered microservices with Django
- **Architecture:** Creates complete ecosystems with Kubernetes, Docker, Helm
- **AI Integration:** BabbleBeaver AI engine for intelligent code generation
- **Infrastructure:** Auto-installs Docker, Kubernetes (Minikube), Helm, kubectl

### Real Setup Process:
```bash
# 1. Clone and setup
git clone https://github.com/buildlyio/buildly-cli.git
cd buildly-cli
chmod +x *.sh

# 2. Launch development environment
source dev.sh
# Interactive menu: Choose 1 (Minikube) → 2 (Helm) → 3 (Buildly Core)

# 3. Generate microservice
./django.sh
# AI prompt interface for service description
# Generates complete Django API + PostgreSQL + K8s deployment
```

### What CLI Actually Generates:
- Complete Django APIs with models, views, serializers
- PostgreSQL database integration  
- Docker containerization
- Kubernetes deployment manifests
- API documentation at /api/docs/
- BabbleBeaver AI framework integration

### Real Architecture:
```
Buildly Labs (Product Management) ↔ Open Source Dev Tools
            ↓                              ↓
    BabbleBeaver AI Engine    →    buildly-cli + Buildly Core
            ↓                              ↓
Frontend (React) ↔ Buildly Core (Gateway) ↔ Microservices (Django)
                            ↓                        ↓
                  Kubernetes Deployment    Database (PostgreSQL)
```

## Actual Buildly Product Labs Information

**Source:** https://docs.buildly.io/docs/quickstart.html

### Key Facts About Product Labs:
- **Purpose:** Product management platform with AI tools powered by BabbleBeaver
- **Target:** Modern development teams and product managers
- **AI Engine:** BabbleBeaver provides intelligent recommendations and automation
- **Integration:** Works with open source developer tools for complete workflow

### Real Setup Process:
1. **Account Registration:** Navigate to organization's Buildly Product Labs instance
2. **Choose Path:** 
   - New Organization: AI-Powered Onboarding at https://labs-onboarding.buildly.io/
   - Existing: Manual registration process
3. **Essential Setup:**
   - Join/Create Teams
   - Configure Notifications
   - Connect Integrations (calendar, project tools)

### Actual Features Available:
- **📊 Product Portfolio:** Project and requirement tracking
- **🗺️ Product Roadmap:** Feature planning and milestone management
- **🚀 Release Management:** Deployment coordination
- **📈 Insights & Analytics:** Performance and metrics monitoring
- **🤖 AI Assistant (BabbleBeaver):** Intelligent project recommendations
- **User Management:** Team collaboration and permissions
- **Profile Settings:** Personal and account preferences

### Real AI Features:
- **BabbleBeaver AI Engine:** Advanced LLM integration with multiple AI model providers
- **AI-Powered Onboarding:** Intelligent setup recommendations
- **Smart Recommendations:** Context-aware project guidance
- **Code Generation:** Via open source buildly-cli and Buildly Core
- **Kubernetes Management:** AI-assisted deployment and service monitoring
- **Privacy & Data Handling:** Enterprise-grade security

## Technical Architecture Facts

### Buildly Core Components:
- **API Gateway:** Service discovery and routing
- **Authentication:** User and service authentication
- **Microservices:** AI-generated Django applications
- **Database:** PostgreSQL for persistent storage
- **Infrastructure:** Kubernetes with Minikube for development

### Development Workflow:
1. **Product Planning:** Use Buildly Product Labs for requirements
2. **Service Generation:** Use CLI to create AI-powered Django APIs
3. **AI Integration:** Configure BabbleBeaver for intelligent features
4. **Deployment:** Kubernetes manifests generated automatically
5. **Monitoring:** Integrated analytics and performance tracking

## Required Accuracy Standards

### DO NOT Fabricate:
- CLI commands that don't exist
- Features not documented in official sources
- Made-up API endpoints or configuration options
- Fictional workflows or processes

### DO Use Real Information:
- Actual CLI scripts: dev.sh, django.sh, fastapi.sh
- Real Product Labs features from docs.buildly.io
- True BabbleBeaver AI capabilities
- Documented architecture patterns
- Verified setup processes

### Verification Sources:
- **Primary:** https://github.com/buildlyio/buildly-cli (CLI documentation)
- **Primary:** https://docs.buildly.io (Platform documentation)
- **Process:** https://radicaltherapy.dev (Development methodology)
- **Community:** Discord and GitHub for support

This reference ensures all future articles contain accurate, verifiable information about the Buildly platform and tools.