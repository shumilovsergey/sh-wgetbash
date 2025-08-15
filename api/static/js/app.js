// WgetBash - Custom JavaScript for enhanced functionality

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Enhanced button hover effects
    initButtonEffects();
    
    // Form validation enhancements
    initFormValidation();
    
    // Alert auto-hide functionality
    initAlertSystem();
    
    // Navigation enhancements
    initNavigationEffects();
});

// Button hover effects
function initButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Form validation enhancements
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let hasErrors = false;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = 'var(--accent-danger)';
                    hasErrors = true;
                } else {
                    field.style.borderColor = 'var(--border-primary)';
                }
            });
            
            if (hasErrors) {
                e.preventDefault();
                showAlert('Пожалуйста, заполните все обязательные поля', 'error');
            }
        });
    });
}

// Alert system
function initAlertSystem() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        if (!alert.classList.contains('hidden')) {
            setTimeout(() => {
                hideAlert(alert);
            }, 5000);
        }
    });
}

// Show alert
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} transition-opacity`;
    alertContainer.innerHTML = `
        <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
        </svg>
        ${message}
    `;
    
    document.body.appendChild(alertContainer);
    
    // Show animation
    setTimeout(() => {
        alertContainer.style.opacity = '1';
    }, 10);
    
    // Auto hide
    setTimeout(() => {
        hideAlert(alertContainer);
    }, 5000);
}

// Hide alert
function hideAlert(alert) {
    alert.style.opacity = '0';
    setTimeout(() => {
        if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }, 300);
}

// Navigation effects
function initNavigationEffects() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // Add loading state
            this.classList.add('loading');
        });
    });
}

// Copy to clipboard with enhanced feedback
function copyToClipboardEnhanced(text, buttonId) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showCopySuccess(buttonId);
        }).catch(() => {
            fallbackCopyTextToClipboard(text, buttonId);
        });
    } else {
        fallbackCopyTextToClipboard(text, buttonId);
    }
}

// Fallback copy method
function fallbackCopyTextToClipboard(text, buttonId) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.position = 'fixed';
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess(buttonId);
    } catch (err) {
        console.error('Fallback: Could not copy text: ', err);
    }
    
    document.body.removeChild(textArea);
}

// Show copy success feedback
function showCopySuccess(buttonId) {
    const button = document.getElementById(buttonId);
    const originalText = button.innerHTML;
    
    button.innerHTML = `
        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        Скопировано!
    `;
    
    button.style.background = 'var(--accent-success)';
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.style.background = '';
    }, 2000);
}

// Enhanced form inputs with floating labels
function initFloatingLabels() {
    const inputs = document.querySelectorAll('.form-input');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Check if input has value on load
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Keyboard shortcuts
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl+S or Cmd+S to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const submitButton = document.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.click();
            }
        }
        
        // Escape to close modals or go back
        if (e.key === 'Escape') {
            const backButton = document.querySelector('a[href*="list"]');
            if (backButton) {
                // Don't auto-navigate on escape - let user decide
                backButton.style.outline = '2px solid var(--accent-primary)';
                setTimeout(() => {
                    backButton.style.outline = '';
                }, 1000);
            }
        }
    });
}

// Dark mode toggle (future enhancement)
function initDarkModeToggle() {
    // Already dark by default, but could add light mode option
    const isDarkMode = localStorage.getItem('darkMode') !== 'false';
    
    if (!isDarkMode) {
        document.body.classList.add('light-mode');
    }
}

// Performance optimizations
function initPerformanceOptimizations() {
    // Lazy load images if any
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

// Initialize all enhancements
document.addEventListener('DOMContentLoaded', function() {
    initFloatingLabels();
    initSmoothScroll();
    initKeyboardShortcuts();
    initDarkModeToggle();
    initPerformanceOptimizations();
});