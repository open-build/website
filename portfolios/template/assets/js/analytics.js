// Portfolio Template JavaScript
// Simple analytics and interaction tracking

// Google Analytics integration (optional)
function initializeAnalytics() {
    // Only initialize if Google Analytics is configured
    if (typeof gtag !== 'undefined') {
        // Track page view
        gtag('config', 'GA_TRACKING_ID', {
            page_title: document.title,
            page_location: window.location.href
        });
    }
}

// Track important interactions
function trackEvent(eventName, parameters = {}) {
    // Google Analytics tracking
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, parameters);
    }
    
    // Console log for development
    console.log('Event tracked:', eventName, parameters);
}

// Track portfolio interactions
function initializePortfolioTracking() {
    // Track project link clicks
    document.querySelectorAll('a[href*="github.com"], a[href*="live-demo"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const projectName = this.closest('.project-card')?.querySelector('h3')?.textContent || 'Unknown Project';
            const linkType = this.href.includes('github.com') ? 'source_code' : 'live_demo';
            
            trackEvent('project_interaction', {
                project_name: projectName,
                link_type: linkType,
                destination_url: this.href
            });
        });
    });
    
    // Track contact form interactions
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            trackEvent('contact_form_submit', {
                form_type: 'contact'
            });
        });
    }
    
    // Track appointment booking clicks
    document.querySelectorAll('a[href*="#appointments"], button[onclick*="appointment"]').forEach(element => {
        element.addEventListener('click', function(e) {
            trackEvent('appointment_interaction', {
                interaction_type: 'booking_attempt'
            });
        });
    });
    
    // Track social media clicks
    document.querySelectorAll('a[href*="github.com"], a[href*="linkedin.com"], a[href*="twitter.com"]').forEach(link => {
        link.addEventListener('click', function(e) {
            let platform = 'unknown';
            if (this.href.includes('github.com')) platform = 'github';
            else if (this.href.includes('linkedin.com')) platform = 'linkedin';
            else if (this.href.includes('twitter.com')) platform = 'twitter';
            
            trackEvent('social_media_click', {
                platform: platform,
                destination_url: this.href
            });
        });
    });
}

// Performance monitoring
function initializePerformanceTracking() {
    // Track page load performance
    window.addEventListener('load', function() {
        if ('performance' in window) {
            const perfData = performance.getEntriesByType('navigation')[0];
            const loadTime = perfData.loadEventEnd - perfData.fetchStart;
            
            trackEvent('page_performance', {
                load_time: Math.round(loadTime),
                dom_content_loaded: Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart),
                first_paint: Math.round(perfData.responseEnd - perfData.fetchStart)
            });
        }
    });
}

// Initialize all tracking when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeAnalytics();
    initializePortfolioTracking();
    initializePerformanceTracking();
});

// Export functions for use in other scripts
window.portfolioAnalytics = {
    trackEvent: trackEvent,
    initializeAnalytics: initializeAnalytics
};
