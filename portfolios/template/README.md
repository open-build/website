# Open Build Developer Portfolio Template

A professional portfolio template for Open Build developers, featuring appointment booking, contact management, and beginner-friendly customization guides.

## 🌟 Features

- **Professional Design**: Built with Tailwind CSS matching Open Build's design system
- **Responsive**: Works perfectly on all devices (mobile, tablet, desktop)
- **Dark Mode**: Toggle between light and dark themes
- **Appointment Booking**: Integrated with Zcal for free scheduling
- **Contact Integration**: All communications cc: team@open.build
- **SEO Optimized**: Meta tags and structured data
- **Fast Loading**: Optimized for performance
- **Accessible**: WCAG compliant design

## 🚀 Quick Start

### 1. Fork This Repository
Click the "Fork" button at the top right of https://github.com/open-build/portfolio-template to create your own copy.

### 2. Clone to Your Computer
```bash
git clone https://github.com/[your-username]/portfolio-template.git
cd portfolio-template
```

### 3. Customize Your Information
Edit `index.html` and replace all `[Your Name]`, `[Your Title]`, etc. with your actual information.

### 4. Deploy to GitHub Pages
1. Go to your repository settings
2. Scroll to "Pages" section
3. Select "Deploy from a branch"
4. Choose "main" branch
5. Your portfolio will be live at: `https://[your-username].github.io/portfolio-template`

## 📝 Customization Guide

### Safe Areas to Edit (Beginner Friendly)

#### ✅ Always Safe to Change:
- Text content (your name, descriptions, etc.)
- Email addresses and links
- Social media links
- Project information
- Colors using Tailwind classes

#### ⚠️ Advanced (Be Careful):
- HTML structure
- CSS classes
- JavaScript functionality

### How to Add Your Information

#### 1. Personal Information
Find and replace these placeholders:
```html
[Your Name] → John Smith
[Your Title] → Full-Stack Developer
[your-email] → john.smith
[your-username] → johnsmith123
[Your Technologies] → React, Node.js, Python
[Your Interests] → AI and Machine Learning
```

#### 2. Add Your Photo
1. Add your photo to `assets/img/profile.jpg`
2. Replace this line:
```html
<i class="fas fa-user text-white text-4xl"></i>
```
With:
```html
<img src="assets/img/profile.jpg" alt="Your Name" class="w-full h-full rounded-full object-cover">
```

#### 3. Add Projects
Copy this template for each project:
```html
<div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 overflow-hidden">
    <div class="h-48 bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
        <img src="path-to-your-project-image.jpg" alt="Project Name" class="w-full h-full object-cover">
    </div>
    <div class="p-6">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">Your Project Name</h3>
        <p class="text-gray-600 dark:text-gray-300 mb-4">
            Description of what your project does and why it's awesome.
        </p>
        <div class="flex flex-wrap gap-2 mb-4">
            <span class="bg-primary text-white px-2 py-1 rounded-full text-xs">React</span>
            <span class="bg-secondary text-white px-2 py-1 rounded-full text-xs">Node.js</span>
        </div>
        <div class="flex space-x-2">
            <a href="https://your-live-demo.com" target="_blank" class="flex-1 bg-primary text-white text-center px-4 py-2 rounded-lg text-sm font-semibold hover:bg-primary-dark transition-colors">
                Live Demo
            </a>
            <a href="https://github.com/your-username/project" target="_blank" class="bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
                <i class="fab fa-github"></i>
            </a>
        </div>
    </div>
</div>
```

## 📅 Setting Up Appointments (Zcal Integration)

### 1. Create Zcal Account
1. Go to [zcal.co](https://zcal.co)
2. Sign up for free account
3. Connect your calendar (Google, Outlook, etc.)

### 2. Get Embed Code
1. Create a new meeting type
2. Set your availability
3. Click "Embed" and copy the iframe code

### 3. Add to Your Portfolio
Replace the placeholder in the appointments section:
```html
<!-- Replace the placeholder div with your Zcal embed -->
<iframe src="https://zcal.co/your-username/30min" width="100%" height="400px" frameborder="0"></iframe>
```

### 4. Email Notifications
Zcal will automatically send notifications to team@open.build when appointments are booked.

## 🎨 Using GitHub Copilot Safely

### General Guidelines for AI Prompts

#### ✅ Good Prompts:
- "Help me add a new project section using the same Tailwind classes as existing projects"
- "Change the primary color but keep all the existing class names"
- "Add a skills section that matches the current design style"

#### ❌ Avoid These Prompts:
- "Rewrite all the HTML" (too broad)
- "Change the entire layout" (might break things)
- "Remove all the classes" (will break styling)

### Safe Prompt Templates

#### Adding Content:
```
"Add a new [section/project/skill] using the same Tailwind CSS classes as the existing ones. Keep the structure similar but change the content to [your specific content]."
```

#### Changing Colors:
```
"Change the color scheme by updating the Tailwind color classes. Keep 'primary' for main actions, 'secondary' for accent colors, and 'accent' for highlights. Use colors: [your preferred colors]"
```

#### Modifying Text:
```
"Update the text content in the [section name] section to reflect my experience as [your role] with skills in [your skills]. Keep all HTML tags and classes the same."
```

### When AI Makes Mistakes:
1. Press `Ctrl+Z` (or `Cmd+Z`) to undo
2. Check that links to Open Build still work
3. Test your site on mobile and desktop
4. Ask AI to "fix the issue but keep it simple"

## 🌐 Custom Domain Setup (Optional)

### Using GitHub Pages with Custom Domain:
1. Buy a domain from any provider (Namecheap, GoDaddy, etc.)
2. In your repository, create a file called `CNAME`
3. Add your domain name to the file: `yourname.dev`
4. Update your domain's DNS settings to point to GitHub Pages
5. Wait 24-48 hours for DNS to propagate

### DNS Settings:
```
Type: CNAME
Name: www
Value: [your-username].github.io

Type: A
Name: @
Values: 
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

## 🔧 Troubleshooting

### Site Not Loading?
- Check that `index.html` is in the root folder
- Verify GitHub Pages is enabled in repository settings
- Wait a few minutes after making changes

### Styling Looks Broken?
- Don't remove Tailwind CSS classes
- Keep the `<script src="https://cdn.tailwindcss.com"></script>` tag
- Check browser console for errors

### Images Not Showing?
- Make sure image files are in the correct folder
- Use relative paths: `assets/img/photo.jpg`
- Check file names match exactly (case-sensitive)

### Contact Form Not Working?
- Add a service like Formspree or Netlify Forms
- The template includes team@open.build cc by default
- Test with a simple mailto: link first

## 📞 Getting Help

### Open Build Community:
- Email: team@open.build
- Visit: [open.build](https://open.build)
- Check out other portfolios for inspiration

### GitHub Issues:
- Create an issue in this repository
- Include screenshots of any problems
- Describe what you were trying to do

### AI Help:
Remember to use safe, specific prompts and always test your changes!

## 📄 License

This template is provided by Open Build for use by program participants. You're free to use and modify it for your personal portfolio.

---

**Built with ❤️ by the Open Build community**

*Portfolio powered by [Open Build](https://open.build) - Training the next generation of developers*
