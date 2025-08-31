from django.urls import path
from . import views_web

urlpatterns = [
    # Landing page
    path('', views_web.landing_view, name='landing'),
    
    # Authentication
    path('login/', views_web.login_view, name='login'),
    path('register/', views_web.register_view, name='register'),
    path('logout/', views_web.logout_view, name='logout'),
    
    # Main pages (require authentication)
    path('dashboard/', views_web.dashboard_view, name='dashboard'),
    path('activities/', views_web.activities_view, name='activities'),
    path('add-activity/', views_web.add_activity_view, name='add_activity'),
    path('profile/', views_web.profile_view, name='profile'),
    
    # Debug
    path('debug/', views_web.debug_static_view, name='debug_static'),
]
