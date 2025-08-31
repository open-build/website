# Open Build Website

A modern, responsive website for Open Build - Software Development Training & Mentorship platform. Built with Tailwind CSS and vanilla JavaScript, designed for GitHub Pages hosting.

## Features

- **Modern Design**: Clean, professional interface with Tailwind CSS
- **Responsive**: Mobile-first design that works on all devices  
- **Interactive Forms**: Contact and application forms with Google Sheets integration
- **Performance Optimized**: Fast loading with optimized assets
- **SEO Friendly**: Semantic HTML with proper meta tags
- **Accessibility**: WCAG compliant with keyboard navigation

## Sections

1. **Hero**: Eye-catching landing section with call-to-actions
2. **Services**: Three main service offerings
   - Junior Developer Program
   - Mentorship Program  
   - Corporate Training
3. **About**: Information about ethical AI and partnerships
4. **Pricing**: Three-tier pricing structure
5. **Application**: Forms for developers and organizations
6. **Contact**: Contact form and information

## Setup Instructions

### 1. GitHub Pages Setup

1. Fork or clone this repository
2. Go to repository Settings > Pages
3. Set source to "Deploy from a branch"
4. Select "main" branch and "/ (root)" folder
5. Your site will be available at `https://username.github.io/repository-name`

### 2. Google Sheets Integration

#### Step 1: Create Google Apps Script

1. Go to [Google Apps Script](https://script.google.com)
2. Create a new project
3. Replace the default code with the contents of `google-apps-script.js`
4. Update the spreadsheet ID in the script to your Google Sheets ID
5. Save the project

#### Step 2: Deploy as Web App

1. Click "Deploy" > "New deployment"
2. Choose type: "Web app"
3. Set execute as: "Me"
4. Set access: "Anyone"
5. Click "Deploy"
6. **Important**: Copy the web app URL (it should look like: `https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec`)

#### Step 3: Update Website Configuration

1. Open `assets/js/main.js`
2. Find the `GOOGLE_SHEETS_CONFIG` object
3. Replace the entire `scriptUrl` value with your web app URL:
   ```javascript
   const GOOGLE_SHEETS_CONFIG = {
       scriptUrl: 'https://script.google.com/macros/s/YOUR_ACTUAL_SCRIPT_ID/exec',
       sheetId: 'YOUR_GOOGLE_SHEETS_ID'
   };
   ```
4. Commit and push changes

#### Troubleshooting Google Sheets Integration

**Common Issues:**

1. **"Google Apps Script URL not configured" error**
   - Make sure you've replaced `YOUR_NEW_SCRIPT_ID` with your actual script ID
   - The URL should be: `https://script.google.com/macros/s/[SCRIPT_ID]/exec`

2. **CORS errors**
   - The Google Apps Script has been updated with proper CORS headers
   - Make sure the script is deployed as a web app with "Anyone" access

3. **Form submissions not working**
   - Check browser console for error messages
   - Test the Google Apps Script URL directly in a browser
   - Verify the Google Sheets ID is correct

4. **Testing the integration**
   - A test button appears in the bottom-right corner for debugging
   - Check browser console for detailed error messages
   - Forms will fallback to email if Google Sheets fails

**Debug Steps:**

1. Open browser developer tools (F12)
2. Go to Console tab
3. Try submitting a form
4. Look for error messages starting with "Google Sheets submission error"
5. Check the Network tab for failed requests

#### Step 4: Set Up Google Sheets

1. Create a new Google Sheets document
2. Copy the sheet ID from the URL (the long string between `/d/` and `/edit`)
3. Update the `sheetId` in `assets/js/main.js`
4. The script will automatically create tabs and headers when first form is submitted

### 3. Customization

#### Colors & Branding

Edit the Tailwind config in `index.html`:
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#2563eb',      // Change primary color
                secondary: '#7c3aed',    // Change secondary color
                accent: '#06b6d4',       // Change accent color
            }
        }
    }
}
```

#### Content Updates

- **Company Information**: Update contact details in the footer and contact section
- **Services**: Modify service descriptions in the services section
- **Pricing**: Update pricing tiers and features
- **Links**: Update partner links (Buildly, First City Foundry)

#### Email Configuration

Update email addresses in:
- `google-apps-script.js`: Change notification email
- Contact section: Update display email

### 4. Optional Enhancements

#### Analytics

Add Google Analytics by including the tracking code in the `<head>` section:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

#### Custom Domain

1. Add a `CNAME` file to the root directory with your domain
2. Configure DNS settings with your domain provider
3. Enable HTTPS in GitHub Pages settings

#### Contact Form Alternatives

If Google Sheets integration doesn't work, the site falls back to:
- mailto links
- You can also integrate with services like Formspree, Netlify Forms, or EmailJS

## File Structure

```
open-build-new-website/
├── index.html                 # Main HTML file
├── assets/
│   ├── css/
│   │   └── style.css         # Custom CSS styles
│   ├── js/
│   │   └── main.js           # JavaScript functionality
│   └── img/                  # Images (add your images here)
├── google-apps-script.js     # Google Apps Script code
├── README.md                 # This file
└── .github/
    └── copilot-instructions.md
```

## Development

### Local Development

1. Clone the repository
2. Open `index.html` in a web browser
3. For live reloading, use a local server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx http-server
   
   # Using PHP
   php -S localhost:8000
   ```

### Making Changes

1. Edit HTML, CSS, or JavaScript files
2. Test changes locally
3. Commit and push to GitHub
4. Changes will automatically deploy to GitHub Pages

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions  
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari, Chrome Mobile

## Performance

The site is optimized for performance:
- Uses CDN for Tailwind CSS and Font Awesome
- Optimized images and assets
- Minimal JavaScript bundle
- CSS animations for smooth interactions

## Security

- Forms use HTTPS for submissions
- Google Apps Script handles server-side processing
- No sensitive data stored client-side
- CSRF protection through Google Apps Script

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or support:
- Email: contact@open.build
- Create an issue in this repository
- Visit: [collab.buildly.io](https://collab.buildly.io)

## Acknowledgments

- Built with [Tailwind CSS](https://tailwindcss.com)
- Icons by [Font Awesome](https://fontawesome.com)
- Hosted on [GitHub Pages](https://pages.github.com)
- Form processing by [Google Apps Script](https://script.google.com)
