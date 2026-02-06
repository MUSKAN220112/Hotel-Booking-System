// Main JavaScript file
console.log('SmartStay Hotel Booking System loaded');

// Format date to YYYY-MM-DD
function formatDate(date) {
    const d = new Date(date);
    let month = String(d.getMonth() + 1).padStart(2, '0');
    let day = String(d.getDate()).padStart(2, '0');
    return [d.getFullYear(), month, day].join('-');
}

// Set minimum check-in date to today
document.addEventListener('DOMContentLoaded', function() {
    const today = formatDate(new Date());
    const checkInInput = document.getElementById('check_in_date');
    const checkOutInput = document.getElementById('check_out_date');
    
    if (checkInInput) {
        checkInInput.setAttribute('min', today);
        checkInInput.addEventListener('change', function() {
            if (checkOutInput) {
                checkOutInput.setAttribute('min', this.value);
            }
        });
    }
});

// API Helper Functions
async function makeRequest(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    
    const container = document.querySelector('.main-content');
    if (container) {
        container.insertBefore(notification, container.firstChild);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Mobile Menu Toggle (if needed)
function setupMobileMenu() {
    const navbarMenu = document.querySelector('.navbar-menu');
    if (navbarMenu && window.innerWidth <= 768) {
        // Add mobile menu functionality here if needed
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', setupMobileMenu);
