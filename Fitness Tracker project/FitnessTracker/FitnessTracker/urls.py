# fitness_tracker/urls.py (main project urls)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('activities.urls')),
]

# activities/urls.py (app urls)
from django.urls import path
from .views import (
    UserRegistrationView,
    CustomAuthToken,
    UserProfileView,
    ActivityListCreateView,
    ActivityDetailView,
    ActivityHistoryView,
    activity_metrics,
    activity_trends,
)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', CustomAuthToken.as_view(), name='user-login'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Activity CRUD endpoints
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    
    # Activity history and metrics
    path('activities/history/', ActivityHistoryView.as_view(), name='activity-history'),
    path('activities/metrics/', activity_metrics, name='activity-metrics'),
    path('activities/trends/', activity_trends, name='activity-trends'),
]