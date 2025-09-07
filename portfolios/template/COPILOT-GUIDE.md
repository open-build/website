# GitHub Copilot Guidelines for Portfolio Customization

## 🤖 Using AI Safely and Effectively

This guide helps you use GitHub Copilot (and other AI assistants) to customize your portfolio without breaking anything.

## ✅ Safe AI Practices

### Golden Rules:
1. **Always be specific** - Don't ask for broad changes
2. **Keep existing structure** - Ask AI to preserve HTML classes and structure
3. **Test after changes** - Check your site after every AI modification
4. **Start small** - Make one change at a time
5. **Keep backups** - Use Git commits before major changes

## 📝 Prompt Templates

### Adding New Projects

**Good Prompt:**
```
Add a new project card to my portfolio. Use the same HTML structure and Tailwind classes as the existing project cards. 

Project details:
- Name: "My E-commerce Website"
- Description: "A modern online store built with React and Node.js"
- Technologies: React, Node.js, MongoDB, Tailwind CSS
- Live URL: https://mystore.example.com
- GitHub URL: https://github.com/username/ecommerce-project

Keep the same styling and responsive design.
```

**Bad Prompt:**
```
Add a project to my portfolio
```
*(Too vague - AI might change too much)*

### Changing Colors

**Good Prompt:**
```
Update the color scheme in my portfolio. Keep all the existing Tailwind CSS classes but change:
- primary color (currently blue) to green
- secondary color (currently purple) to orange
- accent color (currently teal) to red

Only modify the color classes like bg-primary, text-primary, etc. Don't change the layout or structure.
```

**Bad Prompt:**
```
Make it look better with different colors
```
*(AI might change the entire design)*

### Updating Personal Information

**Good Prompt:**
```
Update my personal information in the portfolio:
- Replace "[Your Name]" with "Sarah Johnson"
- Replace "[Your Title]" with "Frontend Developer"
- Replace "[your-email]" with "sarah.johnson"
- Replace "[Your Technologies]" with "React, Vue.js, TypeScript"
- Replace "[Your Interests]" with "User Experience Design"

Keep all HTML tags, CSS classes, and structure exactly the same.
```

### Adding Skills Section

**Good Prompt:**
```
Add a new skill to the skills grid in my about section. Use the same format as existing skills:

Add a skill card for "Python" with:
- Icon: fas fa-python (Font Awesome icon)
- Color: text-green-500 (for the icon)
- Background: bg-gray-50 dark:bg-gray-700 (same as others)
- Text: "Python" (skill name)

Keep the same grid layout and styling as existing skill cards.
```

### Modifying Contact Information

**Good Prompt:**
```
Update my contact information:
- GitHub: github.com/sarah-codes
- LinkedIn: linkedin.com/in/sarah-johnson-dev
- Email: sarah.johnson@open.build

Keep all the existing HTML structure, icons, and Tailwind classes. Only change the URLs and text content.
```

## ⚠️ What to Avoid

### Dangerous Prompts:
```
❌ "Redesign my entire portfolio"
❌ "Make it look modern"  
❌ "Remove all the styling"
❌ "Change the layout completely"
❌ "Rewrite everything in a different framework"
```

### Why These Are Dangerous:
- They're too broad and vague
- AI might remove important functionality
- Could break the responsive design
- Might remove Open Build branding/links
- Could make the site inaccessible

## 🛡️ Safe Zones vs Protected Areas

### ✅ Safe to Modify:
- Text content (names, descriptions, etc.)
- Contact information (email, social links)
- Project information and descriptions
- Color classes (keeping the same structure)
- Image sources and alt text
- Adding new content sections (using existing patterns)

### 🚫 Protected Areas (Be Very Careful):
- HTML structure and layout
- Tailwind CSS class combinations
- JavaScript functionality
- Meta tags and SEO elements
- Open Build branding and links
- Mobile responsive breakpoints

## 🔧 Step-by-Step Customization Process

### 1. Before You Start:
```bash
git add .
git commit -m "Before AI changes - backup"
```

### 2. Make One Change at a Time:
- Start with simple text replacements
- Test in browser after each change
- Commit successful changes

### 3. Use Specific Prompts:
- Include exact details
- Specify what to keep the same
- Ask for one specific modification

### 4. Test Your Changes:
- Check desktop and mobile views
- Test dark mode toggle
- Verify all links work
- Check that forms still function

### 5. If Something Breaks:
```bash
git checkout -- index.html  # Undo changes to index.html
```
Or use `Ctrl+Z` / `Cmd+Z` to undo

## 📱 Testing Checklist

After any AI modifications, check:

- [ ] Site loads without errors
- [ ] Mobile view looks correct
- [ ] Dark mode toggle works
- [ ] All navigation links work
- [ ] Contact form functions
- [ ] Social media links are correct
- [ ] Open Build links still present
- [ ] Images load properly
- [ ] Typography looks consistent

## 🎯 Common Customization Tasks

### Task 1: Adding Your Photo
**Prompt:**
```
Help me replace the placeholder profile image with my actual photo. 

Current code has: <i class="fas fa-user text-white text-4xl"></i>
Replace it with: <img src="assets/img/profile.jpg" alt="Sarah Johnson" class="w-full h-full rounded-full object-cover">

Keep all the surrounding div classes and structure exactly the same.
```

### Task 2: Adding Work Experience
**Prompt:**
```
Add a work experience section to my about area. Create it below the skills section using the same styling patterns.

Experience to add:
- Junior Developer at Tech Corp (2023-Present)
- Intern at StartupXYZ (2022-2023)
- Freelance Web Developer (2021-2022)

Use the same card styling as the skills section with bg-gray-50 dark:bg-gray-700 backgrounds.
```

### Task 3: Customizing the Hero Section
**Prompt:**
```
Update the hero section text to be more personalized:

Change "I build modern web applications..." to:
"I'm passionate about creating accessible web applications that solve real problems. I love turning complex ideas into simple, beautiful user experiences."

Keep all the HTML tags, CSS classes, and surrounding structure exactly the same.
```

## 🆘 When Things Go Wrong

### Common Issues and Fixes:

#### Issue: AI Removed Important Classes
**Fix:** Use `Ctrl+Z` immediately, then try a more specific prompt

#### Issue: Mobile View is Broken
**Fix:** Check that responsive classes (sm:, md:, lg:) weren't removed

#### Issue: Dark Mode Stopped Working  
**Fix:** Verify that `dark:` classes are still present

#### Issue: Links Don't Work
**Fix:** Check that `href` attributes weren't modified incorrectly

### Emergency Recovery:
```bash
# Revert to last working version
git reset --hard HEAD~1

# Or revert specific file
git checkout HEAD~1 -- index.html
```

## 📞 Getting Help

### If You're Stuck:
1. **Check the console**: Open browser dev tools for error messages
2. **Compare with template**: Look at the original template for reference
3. **Ask for help**: Email team@open.build with your issue
4. **Community support**: Check Open Build community resources

### When Asking for Help:
- Include your specific prompt that caused issues
- Share a screenshot of the problem
- Mention what you were trying to achieve
- Include any error messages from browser console

## 🎓 Learning More

### Recommended Learning Path:
1. **HTML Basics**: Understand tags and structure
2. **CSS Basics**: Learn about classes and styling
3. **Tailwind CSS**: Understand utility classes
4. **Git Basics**: Version control for your projects
5. **JavaScript Basics**: For interactive features

### Resources:
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [MDN Web Docs](https://developer.mozilla.org/en-US/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Open Build Learning Resources](https://open.build)

---

**Remember: AI is a powerful tool, but you're in control. Start small, be specific, and always test your changes!**

*Need help? Reach out to team@open.build - we're here to support your learning journey!*
