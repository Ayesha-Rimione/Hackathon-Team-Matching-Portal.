// HackMate - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNotifications();
    initSearchFilters();
    initFormValidation();
    initAnimations();
    initTooltips();
});

// Notification System
function initNotifications() {
    const notificationBadge = document.getElementById('notification-badge');
    
    if (notificationBadge) {
        // Check for unread notifications
        checkUnreadNotifications();
        
        // Update notifications every 30 seconds
        setInterval(checkUnreadNotifications, 30000);
    }
}

function checkUnreadNotifications() {
    const notificationBadge = document.getElementById('notification-badge');
    
    fetch('/api/notifications/unread_count/', {
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.unread_count > 0) {
            notificationBadge.textContent = data.unread_count;
            notificationBadge.style.display = 'inline';
        } else {
            notificationBadge.style.display = 'none';
        }
    })
    .catch(error => {
        console.log('Error checking notifications:', error);
    });
}

// Search and Filter System
function initSearchFilters() {
    const searchInputs = document.querySelectorAll('.search-input');
    const filterSelects = document.querySelectorAll('.filter-select');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(handleSearch, 300));
    });
    
    filterSelects.forEach(select => {
        select.addEventListener('change', handleFilter);
    });
}

function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    const searchableItems = document.querySelectorAll('.searchable-item');
    
    searchableItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

function handleFilter(event) {
    const filterValue = event.target.value;
    const filterableItems = document.querySelectorAll('.filterable-item');
    
    filterableItems.forEach(item => {
        const itemCategory = item.dataset.category;
        if (filterValue === 'all' || itemCategory === filterValue) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Animations
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));
}

// Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// API Helper Functions
const API = {
    // User Management
    async getCurrentUser() {
        try {
            const response = await fetch('/api/users/me/', {
                credentials: 'same-origin'
            });
            return await response.json();
        } catch (error) {
            console.error('Error fetching current user:', error);
            return null;
        }
    },
    
    // Team Management
    async createTeam(teamData) {
        try {
            const response = await fetch('/api/teams/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                credentials: 'same-origin',
                body: JSON.stringify(teamData)
            });
            return await response.json();
        } catch (error) {
            console.error('Error creating team:', error);
            throw error;
        }
    },
    
    async joinTeam(teamId, message = '') {
        try {
            const response = await fetch(`/api/teams/${teamId}/join/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                credentials: 'same-origin',
                body: JSON.stringify({ message })
            });
            return await response.json();
        } catch (error) {
            console.error('Error joining team:', error);
            throw error;
        }
    },
    
    // Event Management
    async registerForEvent(eventId) {
        try {
            const response = await fetch(`/api/events/${eventId}/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                credentials: 'same-origin'
            });
            return await response.json();
        } catch (error) {
            console.error('Error registering for event:', error);
            throw error;
        }
    },
    
    // Messaging
    async sendMessage(conversationId, content) {
        try {
            const response = await fetch('/api/messages/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    conversation: conversationId,
                    content: content
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }
};

// CSRF Token Helper
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// UI Components
const UI = {
    showAlert(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
        alertContainer.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const mainContainer = document.querySelector('main .container');
        if (mainContainer) {
            mainContainer.insertBefore(alertContainer, mainContainer.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (alertContainer.parentNode) {
                    alertContainer.remove();
                }
            }, 5000);
        }
    },
    
    showModal(title, content, buttons = []) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    <div class="modal-footer">
                        ${buttons.map(btn => `
                            <button type="button" class="btn btn-${btn.type || 'secondary'}" 
                                    data-bs-dismiss="modal" ${btn.onClick ? `onclick="${btn.onClick}"` : ''}>
                                ${btn.text}
                            </button>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    },
    
    showLoading(element) {
        element.classList.add('loading');
        element.style.position = 'relative';
    },
    
    hideLoading(element) {
        element.classList.remove('loading');
    }
};

// Event Handlers
document.addEventListener('click', function(event) {
    // Team join button
    if (event.target.matches('.join-team-btn')) {
        event.preventDefault();
        const teamId = event.target.dataset.teamId;
        const teamName = event.target.dataset.teamName;
        
        UI.showModal(
            `Join ${teamName}`,
            `
                <p>Are you sure you want to join this team?</p>
                <div class="mb-3">
                    <label for="join-message" class="form-label">Message (optional)</label>
                    <textarea class="form-control" id="join-message" rows="3" 
                              placeholder="Tell the team why you want to join..."></textarea>
                </div>
            `,
            [
                { text: 'Cancel', type: 'secondary' },
                { 
                    text: 'Join Team', 
                    type: 'primary',
                    onClick: `joinTeam(${teamId})`
                }
            ]
        );
    }
    
    // Event register button
    if (event.target.matches('.register-event-btn')) {
        event.preventDefault();
        const eventId = event.target.dataset.eventId;
        const eventTitle = event.target.dataset.eventTitle;
        
        UI.showModal(
            `Register for ${eventTitle}`,
            `<p>Are you sure you want to register for this event?</p>`,
            [
                { text: 'Cancel', type: 'secondary' },
                { 
                    text: 'Register', 
                    type: 'primary',
                    onClick: `registerForEvent(${eventId})`
                }
            ]
        );
    }
});

// Global functions for modal buttons
function joinTeam(teamId) {
    const message = document.getElementById('join-message')?.value || '';
    
    UI.showLoading(document.body);
    
    API.joinTeam(teamId, message)
        .then(response => {
            UI.hideLoading(document.body);
            if (response.message) {
                UI.showAlert(response.message, 'success');
                // Refresh the page or update UI
                setTimeout(() => location.reload(), 1500);
            }
        })
        .catch(error => {
            UI.hideLoading(document.body);
            UI.showAlert('Error joining team. Please try again.', 'danger');
        });
}

function registerForEvent(eventId) {
    UI.showLoading(document.body);
    
    API.registerForEvent(eventId)
        .then(response => {
            UI.hideLoading(document.body);
            if (response.message) {
                UI.showAlert(response.message, 'success');
                // Refresh the page or update UI
                setTimeout(() => location.reload(), 1500);
            }
        })
        .catch(error => {
            UI.hideLoading(document.body);
            UI.showAlert('Error registering for event. Please try again.', 'danger');
        });
}

// Export for use in other modules
window.HackMate = {
    API,
    UI,
    initNotifications,
    initSearchFilters,
    initFormValidation,
    initAnimations,
    initTooltips
};
