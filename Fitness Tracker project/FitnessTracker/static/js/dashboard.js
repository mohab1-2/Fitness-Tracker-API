// Dashboard page specific JavaScript

// Load dashboard data from API
async function loadDashboardData() {
    try {
        const response = await fetch('/api/activities/metrics/');
        const data = await response.json();
        
        // Update statistics
        updateDashboardStats(data);
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showAlert('Error loading dashboard data', 'error');
    }
}

// Update dashboard statistics
function updateDashboardStats(data) {
    const elements = {
        totalActivities: document.getElementById('totalActivities'),
        totalDuration: document.getElementById('totalDuration'),
        totalDistance: document.getElementById('totalDistance'),
        totalCalories: document.getElementById('totalCalories')
    };
    
    if (elements.totalActivities) {
        elements.totalActivities.textContent = data.activity_count || 0;
    }
    if (elements.totalDuration) {
        elements.totalDuration.textContent = (data.total_duration || 0) + 'm';
    }
    if (elements.totalDistance) {
        elements.totalDistance.textContent = (data.total_distance || 0) + 'km';
    }
    if (elements.totalCalories) {
        elements.totalCalories.textContent = data.total_calories || 0;
    }
}

// Create weekly progress chart
function createWeeklyChart() {
    const ctx = document.getElementById('weeklyProgressChart');
    if (!ctx) return;
    
    // Sample data - replace with real data from API
    const weeklyData = {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            label: 'Duration (minutes)',
            data: [30, 45, 0, 60, 30, 90, 45],
            backgroundColor: 'rgba(102, 126, 234, 0.2)',
            borderColor: 'rgba(102, 126, 234, 1)',
            borderWidth: 2,
            tension: 0.4
        }]
    };
    
    new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: weeklyData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Load recent activities
async function loadRecentActivities() {
    try {
        const response = await fetch('/api/activities/?page_size=5');
        const data = await response.json();
        
        updateRecentActivitiesList(data.results || []);
        
    } catch (error) {
        console.error('Error loading recent activities:', error);
    }
}

// Update recent activities list
function updateRecentActivitiesList(activities) {
    const container = document.getElementById('recentActivities');
    if (!container) return;
    
    if (activities.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-running" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                <p>No activities yet. Start your fitness journey!</p>
                <a href="/add-activity/" class="btn btn-primary">Add Your First Activity</a>
            </div>
        `;
        return;
    }
    
    const activitiesHTML = activities.map(activity => `
        <div class="activity-card mb-2">
            <div class="d-flex justify-between align-center">
                <div>
                    <span class="activity-type ${activity.activity_type}">${activity.activity_type}</span>
                    <h3 class="mb-2">${activity.duration} minutes</h3>
                    <p class="text-muted">
                        <i class="fas fa-route"></i> ${activity.distance} km | 
                        <i class="fas fa-fire"></i> ${activity.calories_burned} cal
                    </p>
                </div>
                <div class="text-right">
                    <small class="text-muted">${formatDate(activity.date)}</small>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = activitiesHTML;
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Load initial data
    loadDashboardData();
    loadRecentActivities();
    createWeeklyChart();
    
    // Refresh data every 5 minutes
    setInterval(loadDashboardData, 300000);
    
    // Add refresh button functionality
    const refreshBtn = document.getElementById('refreshDashboard');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            const originalText = showLoading(this);
            Promise.all([
                loadDashboardData(),
                loadRecentActivities()
            ]).finally(() => {
                hideLoading(this, originalText);
            });
        });
    }
    
    // Add quick action buttons
    const quickActions = document.querySelectorAll('[data-quick-action]');
    quickActions.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.getAttribute('data-quick-action');
            handleQuickAction(action);
        });
    });
});

// Handle quick actions
function handleQuickAction(action) {
    switch (action) {
        case 'add-activity':
            window.location.href = '/add-activity/';
            break;
        case 'view-activities':
            window.location.href = '/activities/';
            break;
        case 'view-profile':
            window.location.href = '/profile/';
            break;
        default:
            console.log('Unknown quick action:', action);
    }
}

// Export functions for use in other modules
window.Dashboard = {
    loadDashboardData,
    updateDashboardStats,
    createWeeklyChart,
    loadRecentActivities,
    updateRecentActivitiesList,
    handleQuickAction
};
