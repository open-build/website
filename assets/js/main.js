// Main JavaScript for Open Build website

// Google Sheets configuration
const GOOGLE_SHEETS_CONFIG = {
    // Google Apps Script Web App URL - UPDATE THIS WITH YOUR NEW DEPLOYMENT URL
    scriptUrl: 'https://script.google.com/macros/s/AKfycbwmuP5Ou5NasZ_RP9wm4sHDgUTsYnI6vJCFyyADRaHIiz87DM6EtwQPCwy4w0F8m_vX/exec',
    sheetId: '1Zu_Ij0vG8Q_ebdjdeFVGY8cDaqyrKIXMoY9qwsgY3JM'
};

// DOM Elements
const navbar = document.querySelector('nav'); // Changed from getElementById('navbar')
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const themeToggle = document.getElementById('theme-toggle');
const applicationModal = document.getElementById('application-modal');
const applicationForm = document.getElementById('application-form');
const contactForm = document.getElementById('contact-form');

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeNavigation();
    initializeFadeInAnimations();
    initializeFormHandlers();
    initializeSmoothScrolling();
});

// Theme functionality
function initializeTheme() {
    // Check for saved theme preference or default to 'light'
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    // Theme toggle event listener
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });
}

// Theme management
function setTheme(theme) {
    const html = document.documentElement;
    const themeIcon = document.getElementById('theme-icon');
    const themeIconDark = document.getElementById('theme-icon-dark');
    
    if (theme === 'dark') {
        html.classList.add('dark');
        themeIcon.classList.add('hidden');
        themeIconDark.classList.remove('hidden');
    } else {
        html.classList.remove('dark');
        themeIcon.classList.remove('hidden');
        themeIconDark.classList.add('hidden');
    }
    
    localStorage.setItem('theme', theme);
}

// Navigation functionality
function initializeNavigation() {
    // Mobile menu toggle
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Navbar scroll effect
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Close mobile menu when clicking on links
    if (mobileMenu) {
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
            });
        });
    }
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Fade-in animations on scroll
function initializeFadeInAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Add fade-in class to elements and observe them
    const animatedElements = document.querySelectorAll('section > div, .icon-box, .pricing-card');
    animatedElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

// Form handlers
function initializeFormHandlers() {
    // Contact form submission
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        handleContactSubmission(this);
    });

    // Application form submission
    applicationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        handleApplicationSubmission(this);
    });
}

// Handle contact form submission
async function handleContactSubmission(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    try {
        // Show loading state
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');

        const formData = new FormData(form);
        const data = {
            type: 'contact',
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message'),
            timestamp: new Date().toISOString(),
            source: 'open-build-website'
        };

        // Send to Google Sheets
        await submitToGoogleSheets(data, 'contacts');
        
        // Show success message
        showMessage('success', 'Thank you! Your message has been sent successfully. We\'ll get back to you soon.');
        form.reset();

    } catch (error) {
        console.error('Error submitting contact form:', error);
        showMessage('error', 'There was an error sending your message. Please try again or contact us directly.');
    } finally {
        // Reset button state
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
    }
}

// Handle application form submission
async function handleApplicationSubmission(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    try {
        // Show loading state
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');

        const formData = new FormData(form);
        const data = {
            type: formData.get('type'),
            name: formData.get('name'),
            email: formData.get('email'),
            experience: formData.get('experience'),
            skills: formData.get('skills'),
            motivation: formData.get('motivation'),
            github: formData.get('github'),
            timestamp: new Date().toISOString(),
            source: 'open-build-website'
        };

        // Send to Google Sheets
        await submitToGoogleSheets(data, 'applications');
        
        // Show success message
        showMessage('success', 'Application submitted successfully! We\'ll review your application and get back to you within 3-5 business days.');
        form.reset();
        closeModal();

    } catch (error) {
        console.error('Error submitting application:', error);
        showMessage('error', 'There was an error submitting your application. Please try again or contact us directly.');
    } finally {
        // Reset button state
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
    }
}

// Submit data to Google Sheets
async function submitToGoogleSheets(data, sheetName) {
    try {
        // Create form data for Google Apps Script
        const formData = new FormData();
        formData.append('sheetName', sheetName);
        formData.append('data', JSON.stringify(data));

        const response = await fetch(GOOGLE_SHEETS_CONFIG.scriptUrl, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Response error text:', errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const result = await response.json();
        console.log('Response result:', result);

        if (result.error) {
            throw new Error(result.error);
        }

        return result;
    } catch (error) {
        console.error('Google Sheets submission error:', error);
        
        // Fallback: try JSONP approach
        try {
            return await submitViaJSONP(data, sheetName);
        } catch (jsonpError) {
            console.error('JSONP fallback failed:', jsonpError);
            
            // Final fallback: open mailto
            const subject = encodeURIComponent(`Open Build ${data.type || 'Contact'} - ${data.name}`);
            const body = encodeURIComponent(JSON.stringify(data, null, 2));
            const mailtoLink = `mailto:contact@open.build?subject=${subject}&body=${body}`;
            
            // Show user the mailto option
            if (confirm('There was an issue submitting your form online. Would you like to send it via email instead?')) {
                window.open(mailtoLink);
            }
            
            throw error;
        }
    }
}

// JSONP fallback for CORS issues
function submitViaJSONP(data, sheetName) {
    return new Promise((resolve, reject) => {
        const callbackName = 'jsonp_callback_' + Math.round(100000 * Math.random());
        
        // Create script element
        const script = document.createElement('script');
        const params = new URLSearchParams({
            callback: callbackName,
            sheetName: sheetName,
            data: JSON.stringify(data)
        });
        
        script.src = `${GOOGLE_SHEETS_CONFIG.scriptUrl}?${params.toString()}`;
        
        // Set up callback
        window[callbackName] = function(response) {
            delete window[callbackName];
            document.body.removeChild(script);
            
            if (response.success) {
                resolve(response);
            } else {
                reject(new Error(response.error || 'Unknown error'));
            }
        };
        
        // Handle errors
        script.onerror = function() {
            delete window[callbackName];
            document.body.removeChild(script);
            reject(new Error('JSONP request failed'));
        };
        
        // Add script to page
        document.body.appendChild(script);
        
        // Timeout after 10 seconds
        setTimeout(() => {
            if (window[callbackName]) {
                delete window[callbackName];
                document.body.removeChild(script);
                reject(new Error('Request timeout'));
            }
        }, 10000);
    });
}

// Modal functions
function openApplicationForm(type) {
    const modal = document.getElementById('application-modal');
    const modalTitle = document.getElementById('modal-title');
    const applicationTypeInput = document.getElementById('application-type');
    
    // Set modal content based on type
    switch(type) {
        case 'individual':
        case 'developer':
            modalTitle.textContent = 'Developer Application';
            applicationTypeInput.value = 'developer';
            break;
        case 'mentor':
            modalTitle.textContent = 'Mentor Application';
            applicationTypeInput.value = 'mentor';
            break;
        default:
            modalTitle.textContent = 'Application';
            applicationTypeInput.value = type;
    }
    
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function openContactForm(planType) {
    // Scroll to contact section and pre-fill subject
    const contactSection = document.getElementById('contact');
    const subjectSelect = document.getElementById('subject');
    
    contactSection.scrollIntoView({ behavior: 'smooth' });
    
    // Set subject based on plan type
    setTimeout(() => {
        switch(planType) {
            case 'startup':
                subjectSelect.value = 'corporate-training';
                break;
            case 'enterprise':
                subjectSelect.value = 'corporate-training';
                break;
            case 'organization':
                subjectSelect.value = 'corporate-training';
                break;
            default:
                subjectSelect.value = 'general';
        }
    }, 500);
}

function closeModal() {
    const modal = document.getElementById('application-modal');
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
    
    // Reset form
    document.getElementById('application-form').reset();
}

// Close modal when clicking outside
document.getElementById('application-modal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Show success/error messages
function showMessage(type, message) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.success-message, .error-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `${type}-message`;
    messageDiv.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} mr-3"></i>
                <span>${message}</span>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    messageDiv.style.display = 'block';
    
    // Add to contact form or modal
    const activeForm = document.querySelector('#application-modal:not(.hidden)') ? 
        document.getElementById('application-form') : 
        document.getElementById('contact-form');
    
    activeForm.appendChild(messageDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}

// Analytics and tracking (optional)
function trackEvent(eventName, properties = {}) {
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, properties);
    }
    
    // Console log for development
    console.log('Event tracked:', eventName, properties);
}

// Track form submissions
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.id === 'contact-form') {
        trackEvent('contact_form_submit', {
            subject: form.subject.value
        });
    } else if (form.id === 'application-form') {
        trackEvent('application_submit', {
            type: form.type.value,
            experience: form.experience.value
        });
    }
});

// Track CTA clicks
document.addEventListener('click', function(e) {
    const target = e.target.closest('a, button');
    if (!target) return;
    
    const text = target.textContent.trim();
    const href = target.href;
    
    // Track external links
    if (href && (href.includes('buildly.io') || href.includes('firstcityfoundry.com'))) {
        trackEvent('external_link_click', {
            url: href,
            text: text
        });
    }
    
    // Track CTA buttons
    if (target.classList.contains('bg-primary') || target.classList.contains('bg-secondary')) {
        trackEvent('cta_click', {
            text: text,
            section: target.closest('section')?.id || 'unknown'
        });
    }
});

// Test Google Apps Script connection
async function testGoogleAppsScript() {
    try {
        console.log('Testing Google Apps Script connection...');

        const response = await fetch(GOOGLE_SHEETS_CONFIG.scriptUrl, {
            method: 'GET'
        });

        const result = await response.json();
        console.log('Test result:', result);
        alert('Google Apps Script is working! Response: ' + JSON.stringify(result));
    } catch (error) {
        console.error('Test failed:', error);
        alert('Google Apps Script test failed: ' + error.message);
    }
}

// Add test button to page (for debugging)
document.addEventListener('DOMContentLoaded', function() {
    // Add test button for debugging (remove in production)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        const testButton = document.createElement('button');
        testButton.textContent = 'Test Google Apps Script';
        testButton.style.position = 'fixed';
        testButton.style.bottom = '20px';
        testButton.style.right = '20px';
        testButton.style.zIndex = '9999';
        testButton.style.padding = '10px';
        testButton.style.background = '#4285f4';
        testButton.style.color = 'white';
        testButton.style.border = 'none';
        testButton.style.borderRadius = '5px';
        testButton.style.cursor = 'pointer';
        testButton.onclick = testGoogleAppsScript;
        document.body.appendChild(testButton);
    }
});

// Service Worker registration (for offline functionality)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}
