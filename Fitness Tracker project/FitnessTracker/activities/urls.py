from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    # Activity CRUD endpoints
    path('activities/', views.ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', views.ActivityDetailView.as_view(), name='activity-detail'),
    
    # Activity history and metrics endpoints
    path('activities/history/', views.activity_history, name='activity-history'),
    path('activities/metrics/', views.activity_metrics, name='activity-metrics'),
]
