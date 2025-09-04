# Portfolio Template Repository Setup Instructions

## Files to Create in New Repository: `open-build/portfolio-template`

### 1. Root Files:
```
portfolio-template/
├── index.html (main portfolio page)
├── README.md (setup guide)
├── COPILOT-GUIDE.md (AI usage guide)
├── LICENSE (MIT License)
├── .gitignore (standard web project)
└── _config.yml (GitHub Pages config)
```

### 2. Directory Structure:
```
assets/
├── css/
│   └── custom.css (additional styles if needed)
├── js/
│   ├── main.js (portfolio functionality)
│   └── analytics.js (optional tracking)
├── img/
│   ├── favicon.png
│   ├── apple-touch-icon.png
│   └── placeholder-profile.jpg
└── contracts/
    └── template-contract.pdf (basic contract template)

docs/
├── setup-guide.md (detailed setup)
├── zcal-integration.md (appointment booking setup)
├── copilot-examples.md (AI prompt examples)
└── customization-guide.md (safe customization)

examples/
├── beginner-portfolio/ (simple example)
├── intermediate-portfolio/ (more features)
└── advanced-portfolio/ (full-featured)

.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
├── workflows/
│   └── pages-deploy.yml (auto-deploy)
└── FUNDING.yml (Open Build donation links)
```

## Step-by-Step Repository Creation:

### 1. Create Repository on GitHub:
1. Go to https://github.com/orgs/open-build/repositories
2. Click "New repository"
3. Repository name: `portfolio-template`
4. Description: "Professional portfolio template for Open Build developers with appointment booking and AI-safe customization guides"
5. Make it Public
6. ✅ Add a README file
7. Choose MIT License
8. ✅ Use this repository as a template (IMPORTANT!)

### 2. Clone and Set Up Locally:
```bash
git clone https://github.com/open-build/portfolio-template.git
cd portfolio-template
```

### 3. Copy Files from Current Project:
Copy these files from `/home/glind/Projects/open_build/website/website/portfolios/template/`:
- `index.html` → root directory
- `README.md` → root directory  
- `COPILOT-GUIDE.md` → root directory

### 4. Enable GitHub Pages:
1. Go to repository Settings
2. Scroll to Pages section
3. Source: "Deploy from a branch"
4. Branch: "main" 
5. Folder: "/ (root)"
6. Save

### 5. Enable Template Repository:
1. Go to repository Settings
2. Scroll to "Template repository"
3. ✅ Check "Template repository"
4. This allows others to use "Use this template" button

## Repository Settings Configuration:

### About Section:
- **Description**: "Professional portfolio template for Open Build developers"
- **Website**: https://open.build
- **Topics**: `portfolio`, `template`, `open-build`, `tailwindcss`, `github-pages`, `developer-portfolio`

### Repository Rules:
- ✅ Allow merge commits
- ✅ Allow squash merging  
- ✅ Allow rebase merging
- ✅ Automatically delete head branches

### Security:
- ✅ Enable vulnerability alerts
- ✅ Enable Dependabot security updates

## Files Content Overview:

The repository should contain:
1. **Complete Portfolio Template**: Ready-to-use HTML with Tailwind CSS
2. **Comprehensive Documentation**: Setup guides in English (Spanish later)
3. **AI Safety Guidelines**: Copilot prompts and constraints
4. **Business Integration**: Zcal setup, contract templates
5. **Examples**: Different complexity levels for various skill levels
6. **Automation**: GitHub Actions for easy deployment

## Post-Creation Tasks:

### 1. Test the Template:
1. Fork the repository (test forking works)
2. Deploy to GitHub Pages (verify deployment)
3. Test all links and functionality
4. Verify mobile responsiveness

### 2. Update Main Website:
- Links should point to new repository
- Test fork button functionality
- Update portfolio showcase examples

### 3. Documentation:
- Create video walkthrough (optional)
- Add to Open Build main documentation
- Share with community for testing

### 4. Community Integration:
- Announce in Open Build channels
- Create example portfolios using the template
- Gather feedback and iterate

## Template Repository Features:

### For Repository Visitors:
- Big green "Use this template" button
- Clear README with quick start
- Live demo link (GitHub Pages)
- Comprehensive documentation

### For Open Build Developers:
- One-click portfolio creation
- Built-in Open Build branding
- Automated team@open.build integration
- Safe AI customization guides
- Professional design matching main site

### For Open Build Organization:
- Showcases developer capabilities
- Maintains consistent branding
- Generates leads through portfolio contact forms
- Builds community around shared template

---

**Next Steps:**
1. Create the repository using these specifications
2. Copy and commit all template files
3. Enable template and pages features
4. Test the complete workflow
5. Update main website links to point to new repo

Let me know when the repository is created and I'll help with any additional setup or modifications needed!
