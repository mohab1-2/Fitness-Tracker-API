// Add Activity page specific JavaScript

// Set default date to current date/time
function setDefaultDate() {
    const now = new Date();
    const localDate = new Date(now.getTime() - now.getTimezoneOffset() * 60000);
    const dateInput = document.getElementById('date');
    if (dateInput) {
        dateInput.value = localDate.toISOString().slice(0, 16);
    }
}

// Form validation
function initializeFormValidation() {
    const form = document.getElementById('addActivityForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateActivityForm()) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = showLoading(submitBtn);
            
            // Submit form
            this.submit();
        }
    });
}

function validateActivityForm() {
    const duration = parseInt(document.getElementById('duration').value);
    const distance = parseFloat(document.getElementById('distance').value);
    const calories = parseInt(document.getElementById('calories_burned').value);
    
    // Validation
    if (duration < 1 || duration > 1440) {
        showAlert('Duration must be between 1 and 1440 minutes', 'error');
        return false;
    }
    
    if (distance < 0) {
        showAlert('Distance cannot be negative', 'error');
        return false;
    }
    
    if (calories < 0) {
        showAlert('Calories cannot be negative', 'error');
        return false;
    }
    
    return true;
}

// Quick add templates
function fillTemplate(activityType, duration, distance, calories) {
    document.getElementById('activity_type').value = activityType;
    document.getElementById('duration').value = duration;
    document.getElementById('distance').value = distance;
    document.getElementById('calories_burned').value = calories;
    
    // Set current date/time
    setDefaultDate();
    
    showAlert(`${activityType} template loaded!`, 'success');
}

// Real-time validation
function initializeRealTimeValidation() {
    const durationInput = document.getElementById('duration');
    const distanceInput = document.getElementById('distance');
    const caloriesInput = document.getElementById('calories_burned');
    
    if (durationInput) {
        durationInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value < 1 || value > 1440) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#e9ecef';
            }
        });
    }
    
    if (distanceInput) {
        distanceInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value < 0) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#e9ecef';
            }
        });
    }
    
    if (caloriesInput) {
        caloriesInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value < 0) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#e9ecef';
            }
        });
    }
}

// Auto-calculate calories based on activity type and duration
function initializeCalorieCalculation() {
    const activityTypeSelect = document.getElementById('activity_type');
    const durationInput = document.getElementById('duration');
    const caloriesInput = document.getElementById('calories_burned');
    
    if (!activityTypeSelect || !durationInput || !caloriesInput) return;
    
    const calorieRates = {
        running: 10,      // calories per minute
        cycling: 8,
        weightlifting: 6,
        swimming: 9,
        walking: 4,
        yoga: 3,
        other: 5
    };
    
    function calculateCalories() {
        const activityType = activityTypeSelect.value;
        const duration = parseInt(durationInput.value) || 0;
        
        if (activityType && duration > 0) {
            const rate = calorieRates[activityType] || calorieRates.other;
            const calculatedCalories = Math.round(duration * rate);
            caloriesInput.value = calculatedCalories;
        }
    }
    
    activityTypeSelect.addEventListener('change', calculateCalories);
    durationInput.addEventListener('input', calculateCalories);
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    setDefaultDate();
    initializeFormValidation();
    initializeRealTimeValidation();
    initializeCalorieCalculation();
    
    // Add template button event listeners
    const templateButtons = document.querySelectorAll('[data-template]');
    templateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const template = this.getAttribute('data-template');
            const templates = {
                'running-30': ['running', 30, 5, 300],
                'cycling-45': ['cycling', 45, 15, 450],
                'weightlifting-60': ['weightlifting', 60, 0, 400],
                'walking-20': ['walking', 20, 2, 120],
                'swimming-30': ['swimming', 30, 1, 250],
                'yoga-45': ['yoga', 45, 0, 150]
            };
            
            if (templates[template]) {
                fillTemplate(...templates[template]);
            }
        });
    });
});

// Export functions for use in other modules
window.AddActivity = {
    setDefaultDate,
    validateActivityForm,
    fillTemplate,
    initializeFormValidation,
    initializeRealTimeValidation,
    initializeCalorieCalculation
};
