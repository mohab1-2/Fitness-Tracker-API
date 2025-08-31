# Fitness Tracker Frontend

A beautiful, modern web interface for the Fitness Tracker Django application with separate CSS and JavaScript files for better organization and maintainability.

## 📁 File Structure

```
FitnessTracker/
├── static/
│   ├── css/
│   │   └── style.css              # Main stylesheet with all CSS
│   └── js/
│       ├── main.js                # Common JavaScript functions
│       ├── dashboard.js           # Dashboard page functionality
│       ├── activities.js          # Activities page functionality
│       └── add-activity.js        # Add activity page functionality
├── templates/
│   ├── base.html                  # Base template with navigation
│   ├── landing.html               # Welcome page
│   ├── login.html                 # Login form
│   ├── register.html              # Registration form
│   ├── dashboard.html             # User dashboard
│   ├── activities.html            # Activities list and management
│   ├── add_activity.html          # Add new activity form
│   └── profile.html               # User profile page
└── README.md                      # This file
```

## 🎨 CSS Files

### `static/css/style.css`
The main stylesheet containing all the styling for the application:

- **Reset and Base Styles**: CSS reset and basic body styling
- **Navigation**: Navbar styling with backdrop blur effect
- **Layout Components**: Cards, grids, and containers
- **Buttons**: Primary and secondary button styles with hover effects
- **Forms**: Input fields, labels, and form groups
- **Alerts**: Success and error message styling
- **Activity Cards**: Styling for activity display cards
- **Statistics Grid**: Dashboard statistics layout
- **Responsive Design**: Mobile-first responsive breakpoints
- **Utility Classes**: Helper classes for spacing, alignment, etc.

## 🚀 JavaScript Files

### `static/js/main.js`
Common JavaScript functions used across all pages:

- **Loading States**: `showLoading()`, `hideLoading()`
- **Alert System**: `showAlert()` for notifications
- **Date Formatting**: `formatDate()`, `formatDuration()`, `formatDistance()`
- **Form Validation**: `validatePassword()`, `validateEmail()`, `validateNumber()`
- **API Utilities**: `apiRequest()`, `getCSRFToken()`
- **Modal Management**: `showModal()`, `hideModal()`
- **Chart Utilities**: `createChart()` for Chart.js integration
- **Local Storage**: `saveToLocalStorage()`, `getFromLocalStorage()`
- **Utility Functions**: `debounce()`, `throttle()`

### `static/js/dashboard.js`
Dashboard-specific functionality:

- **Data Loading**: `loadDashboardData()`, `loadRecentActivities()`
- **Statistics Updates**: `updateDashboardStats()`
- **Chart Creation**: `createWeeklyChart()` for progress visualization
- **Activity Lists**: `updateRecentActivitiesList()`
- **Auto-refresh**: Automatic data refresh every 5 minutes

### `static/js/activities.js`
Activities page functionality:

- **Filtering**: `applyFilters()`, `clearFilters()`
- **Activity Management**: `editActivity()`, `deleteActivity()`, `updateActivity()`
- **Modal Handling**: `populateEditForm()`, `closeEditModal()`
- **Search**: `performSearch()` with debounced input
- **Pagination**: `initializePagination()`
- **Bulk Actions**: `performBulkAction()` for multiple activities

### `static/js/add-activity.js`
Add activity page functionality:

- **Form Validation**: `validateActivityForm()`
- **Template System**: `fillTemplate()` for quick activity templates
- **Real-time Validation**: Input validation with visual feedback
- **Auto-calculation**: `initializeCalorieCalculation()` based on activity type
- **Date Handling**: `setDefaultDate()` for current date/time

## 🔧 Usage

### Including CSS
```html
{% load static %}
<link href="{% static 'css/style.css' %}" rel="stylesheet">
```

### Including JavaScript
```html
<!-- Main JavaScript (included in base.html) -->
<script src="{% static 'js/main.js' %}"></script>

<!-- Page-specific JavaScript -->
<script src="{% static 'js/dashboard.js' %}"></script>
<script src="{% static 'js/activities.js' %}"></script>
<script src="{% static 'js/add-activity.js' %}"></script>
```

## 🎯 Features

### CSS Features
- **Modern Design**: Clean, professional interface with gradients and shadows
- **Responsive**: Mobile-first design that works on all devices
- **Flexible Grid**: CSS Grid and Flexbox for dynamic layouts
- **Smooth Animations**: Hover effects and transitions
- **Color-coded Activities**: Different colors for each activity type
- **Accessibility**: High contrast and readable typography

### JavaScript Features
- **Modular Architecture**: Separate files for different page functionalities
- **Error Handling**: Comprehensive error handling and user feedback
- **Performance**: Debounced search, throttled events
- **API Integration**: Seamless communication with Django REST API
- **Form Validation**: Client-side and real-time validation
- **Interactive Charts**: Chart.js integration for data visualization
- **Local Storage**: Caching and user preferences

## 🚀 Benefits of Separate Files

1. **Maintainability**: Easier to find and modify specific functionality
2. **Performance**: Better caching and loading optimization
3. **Reusability**: Common functions can be shared across pages
4. **Debugging**: Easier to debug specific page issues
5. **Team Development**: Multiple developers can work on different files
6. **Code Organization**: Clear separation of concerns
7. **Scalability**: Easy to add new pages and functionality

## 📱 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🔧 Development

To modify the styling or functionality:

1. **CSS Changes**: Edit `static/css/style.css`
2. **Common JS**: Edit `static/css/main.js`
3. **Page-specific JS**: Edit the corresponding page JavaScript file
4. **Test**: Refresh the page to see changes immediately

## 📝 Notes

- All JavaScript files are loaded after the main.js file
- CSS is loaded in the head section for better performance
- External libraries (Chart.js, Font Awesome) are loaded from CDN
- The application uses Django's static file handling
- All functions are properly namespaced to avoid conflicts
