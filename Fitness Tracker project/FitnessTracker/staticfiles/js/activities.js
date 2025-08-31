// Activities page specific JavaScript

let currentActivityId = null;

// Filter functionality
function initializeFilters() {
    const applyFiltersBtn = document.getElementById('applyFilters');
    const clearFiltersBtn = document.getElementById('clearFilters');
    
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', applyFilters);
    }
    
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', clearFilters);
    }
    
    // Set current filter values from URL params
    setFilterValuesFromURL();
}

function applyFilters() {
    const form = document.getElementById('filterForm');
    const formData = new FormData(form);
    const params = new URLSearchParams();
    
    for (let [key, value] of formData.entries()) {
        if (value) {
            params.append(key, value);
        }
    }
    
    window.location.href = `/activities/?${params.toString()}`;
}

function clearFilters() {
    document.getElementById('filterForm').reset();
    window.location.href = '/activities/';
}

function setFilterValuesFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    
    const activityType = urlParams.get('activity_type');
    const startDate = urlParams.get('start_date');
    const endDate = urlParams.get('end_date');
    
    if (activityType) {
        document.getElementById('activityType').value = activityType;
    }
    if (startDate) {
        document.getElementById('startDate').value = startDate;
    }
    if (endDate) {
        document.getElementById('endDate').value = endDate;
    }
}

// Edit activity functionality
function editActivity(activityId) {
    currentActivityId = activityId;
    
    // Fetch activity data
    fetch(`/api/activities/${activityId}/`)
        .then(response => response.json())
        .then(data => {
            populateEditForm(data);
            showModal('editModal');
        })
        .catch(error => {
            console.error('Error loading activity data:', error);
            showAlert('Error loading activity data', 'error');
        });
}

function populateEditForm(data) {
    document.getElementById('editActivityType').value = data.activity_type;
    document.getElementById('editDuration').value = data.duration;
    document.getElementById('editDistance').value = data.distance;
    document.getElementById('editCalories').value = data.calories_burned;
    
    // Format date for datetime-local input
    const date = new Date(data.date);
    const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
    document.getElementById('editDate').value = localDate.toISOString().slice(0, 16);
}

function closeEditModal() {
    hideModal('editModal');
    currentActivityId = null;
}

// Update activity
function initializeEditForm() {
    const editForm = document.getElementById('editForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            updateActivity();
        });
    }
}

async function updateActivity() {
    if (!currentActivityId) return;
    
    const form = document.getElementById('editForm');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch(`/api/activities/${currentActivityId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('Activity updated successfully!');
            closeEditModal();
            location.reload();
        } else {
            throw new Error('Failed to update activity');
        }
    } catch (error) {
        console.error('Error updating activity:', error);
        showAlert('Error updating activity', 'error');
    }
}

// Delete activity
function deleteActivity(activityId) {
    if (confirm('Are you sure you want to delete this activity?')) {
        fetch(`/api/activities/${activityId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => {
            if (response.ok) {
                showAlert('Activity deleted successfully!');
                location.reload();
            } else {
                throw new Error('Failed to delete activity');
            }
        })
        .catch(error => {
            console.error('Error deleting activity:', error);
            showAlert('Error deleting activity', 'error');
        });
    }
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        const debouncedSearch = debounce(performSearch, 300);
        searchInput.addEventListener('input', debouncedSearch);
    }
}

function performSearch() {
    const searchTerm = document.getElementById('searchInput').value;
    const currentUrl = new URL(window.location);
    
    if (searchTerm) {
        currentUrl.searchParams.set('search', searchTerm);
    } else {
        currentUrl.searchParams.delete('search');
    }
    
    window.location.href = currentUrl.toString();
}

// Pagination
function initializePagination() {
    const paginationLinks = document.querySelectorAll('.pagination a');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            if (page) {
                const currentUrl = new URL(window.location);
                currentUrl.searchParams.set('page', page);
                window.location.href = currentUrl.toString();
            }
        });
    });
}

// Activity card interactions
function initializeActivityCards() {
    // Add hover effects and click handlers
    const activityCards = document.querySelectorAll('.activity-card');
    activityCards.forEach(card => {
        card.addEventListener('click', function() {
            const activityId = this.getAttribute('data-activity-id');
            if (activityId) {
                // Could open a detailed view modal here
                console.log('Activity clicked:', activityId);
            }
        });
    });
}

// Export functions
function exportActivities(format = 'csv') {
    const currentUrl = new URL(window.location);
    currentUrl.searchParams.set('export', format);
    
    window.open(currentUrl.toString(), '_blank');
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    initializeFilters();
    initializeEditForm();
    initializeSearch();
    initializePagination();
    initializeActivityCards();
    
    // Add export functionality
    const exportButtons = document.querySelectorAll('[data-export]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            exportActivities(format);
        });
    });
    
    // Add bulk actions
    const bulkActionForm = document.getElementById('bulkActionForm');
    if (bulkActionForm) {
        bulkActionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const action = document.getElementById('bulkAction').value;
            const selectedActivities = getSelectedActivities();
            
            if (selectedActivities.length === 0) {
                showAlert('Please select activities to perform bulk action', 'error');
                return;
            }
            
            performBulkAction(action, selectedActivities);
        });
    }
});

// Bulk actions
function getSelectedActivities() {
    const checkboxes = document.querySelectorAll('input[name="activity_ids"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

function performBulkAction(action, activityIds) {
    if (action === 'delete') {
        if (confirm(`Are you sure you want to delete ${activityIds.length} activities?`)) {
            // Implement bulk delete
            console.log('Bulk delete:', activityIds);
        }
    } else if (action === 'export') {
        // Implement bulk export
        console.log('Bulk export:', activityIds);
    }
}

// Export functions for use in other modules
window.Activities = {
    editActivity,
    deleteActivity,
    updateActivity,
    closeEditModal,
    applyFilters,
    clearFilters,
    exportActivities,
    performBulkAction
};
