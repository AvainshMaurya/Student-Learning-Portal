/**
 * Student Learning Portal - Main JavaScript File
 * Handles dark mode, interactive features, and UI enhancements
 */

// ============ DARK MODE TOGGLE ============
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark mode
    initDarkMode();
    
    // Set up event listeners
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }
});

function initDarkMode() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        updateDarkModeIcon(true);
    }
}

function toggleDarkMode() {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
    updateDarkModeIcon(isDarkMode);
}

function updateDarkModeIcon(isDarkMode) {
    const icon = document.getElementById('darkModeToggle').querySelector('i');
    if (isDarkMode) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
}

// ============ FORM HANDLING ============
/**
 * Handle AJAX form submission with validation
 */
function submitFormAjax(formId, endpoint, redirectUrl = null, onSuccess = null) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                showSuccessAlert(result.message);
                if (onSuccess) {
                    onSuccess(result);
                }
                if (redirectUrl) {
                    setTimeout(() => {
                        window.location.href = redirectUrl;
                    }, 1500);
                }
            } else {
                showErrorAlert(result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            showErrorAlert('An error occurred. Please try again.');
        }
    });
}

// ============ NOTIFICATIONS ============
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show m-3`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.body;
    container.insertBefore(alertDiv, container.firstChild);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showSuccessAlert(message) {
    showAlert(message, 'success');
}

function showErrorAlert(message) {
    showAlert(message, 'danger');
}

function showInfoAlert(message) {
    showAlert(message, 'info');
}

// ============ SEARCH FUNCTIONALITY ============
/**
 * Real-time search filtering
 */
function initSearchFilter(searchInputId, filterContainerId, itemSelector) {
    const searchInput = document.getElementById(searchInputId);
    if (!searchInput) return;

    searchInput.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const items = document.querySelectorAll(itemSelector);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(searchTerm) ? 'block' : 'none';
        });
    });
}

// ============ TABLE FUNCTIONALITY ============
/**
 * Make tables responsive and sortable
 */
function initResponseTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;

    // Add responsive wrapper
    if (!table.closest('.table-responsive')) {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-responsive';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    }
}

// ============ LAZY LOADING ============
/**
 * Lazy load images
 */
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// ============ NAVBAR SCROLL EFFECT ============
/**
 * Add shadow to navbar on scroll
 */
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 0) {
            navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
        }
    }
});

// ============ FORM VALIDATION ============
/**
 * Bootstrap form validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!this.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            this.classList.add('was-validated');
        }, false);
    });
}

// Initialize form validation on page load
document.addEventListener('DOMContentLoaded', initFormValidation);

// ============ TOOLTIP INITIALIZATION ============
/**
 * Initialize Bootstrap tooltips
 */
document.addEventListener('DOMContentLoaded', function() {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
});

// ============ MODAL FUNCTIONALITY ============
/**
 * Show modal with message
 */
function showModal(title, message, buttons = null) {
    const modalHtml = `
        <div class="modal fade" id="customModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${message}
                    </div>
                    <div class="modal-footer">
                        ${buttons ? buttons : '<button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>'}
                    </div>
                </div>
            </div>
        </div>
    `;

    const modalElement = document.createElement('div');
    modalElement.innerHTML = modalHtml;
    document.body.appendChild(modalElement);

    const modal = new bootstrap.Modal(document.getElementById('customModal'));
    modal.show();

    // Clean up after modal is hidden
    document.getElementById('customModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// ============ UTILITY FUNCTIONS ============
/**
 * Format date to readable format
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Format time in seconds to MM:SS
 */
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

/**
 * Format percentage
 */
function formatPercentage(value) {
    return `${Math.round(value)}%`;
}

/**
 * Get query parameter from URL
 */
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

/**
 * Set query parameter in URL
 */
function setQueryParam(param, value) {
    const url = new URL(window.location);
    url.searchParams.set(param, value);
    window.history.pushState({}, '', url);
}

// ============ PRINT FUNCTIONALITY ============
/**
 * Print page
 */
function printPage() {
    window.print();
}

/**
 * Export data to CSV
 */
function exportToCSV(data, filename) {
    const csv = [Object.keys(data[0]).join(',')];
    data.forEach(row => {
        csv.push(Object.values(row).join(','));
    });

    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

// ============ LOCAL STORAGE HELPERS ============
/**
 * Save data to local storage
 */
function saveToLocalStorage(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

/**
 * Get data from local storage
 */
function getFromLocalStorage(key) {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

/**
 * Remove data from local storage
 */
function removeFromLocalStorage(key) {
    localStorage.removeItem(key);
}

// ============ DEBOUNCE FUNCTION ============
/**
 * Debounce function to prevent excessive function calls
 */
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

// ============ API HELPER ============
/**
 * Make API call
 */
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API error:', error);
        throw error;
    }
}

// ============ PAGE READY ============
/**
 * Initialize lazy loading and other features
 */
document.addEventListener('DOMContentLoaded', function() {
    initLazyLoading();
});

// ============ SMOOTH SCROLL ============
/**
 * Smooth scroll to anchor
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============ PREVENT DOUBLE SUBMIT ============
/**
 * Prevent double form submission
 */
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitButton = form.querySelector('[type="submit"]');
    
    if (submitButton && !form.classList.contains('submitted')) {
        form.classList.add('submitted');
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    }
});
