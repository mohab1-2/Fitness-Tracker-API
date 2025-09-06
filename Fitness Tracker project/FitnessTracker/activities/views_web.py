from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Sum
from django.http import JsonResponse
from .models import Activity, User
from .forms import ActivityForm
import json
from datetime import datetime, timedelta
from django.utils import timezone

def landing_view(request):
    """Landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

@csrf_protect
@never_cache
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
    return render(request, 'login.html')

@csrf_protect
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Account created successfully! Welcome, {user.username}!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred while creating your account. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    """User logout view"""
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye {username}! You have been logged out successfully.')
    return redirect('landing')

@login_required
def dashboard_view(request):
    """User dashboard view"""
    try:
        # Get user's activities
        activities = Activity.objects.filter(user=request.user).order_by('-date')
        
        # Calculate statistics
        stats = {
            'total_activities': activities.count(),
            'total_duration': activities.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance': activities.aggregate(Sum('distance'))['distance__sum'] or 0,
            'total_calories': activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
        }
        
        # Get recent activities
        recent_activities = activities[:5]
        
        # Get activity distribution
        activity_distribution = activities.values('activity_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context = {
            'stats': stats,
            'recent_activities': recent_activities,
            'activity_distribution': activity_distribution,
        }
    except Exception as e:
        messages.error(request, 'Error loading dashboard data. Please try again.')
        context = {
            'stats': {'total_activities': 0, 'total_duration': 0, 'total_distance': 0, 'total_calories': 0},
            'recent_activities': [],
            'activity_distribution': [],
        }
    
    return render(request, 'dashboard.html', context)

@login_required
def activities_view(request):
    """Activities list view with filtering and pagination"""
    try:
        activities = Activity.objects.filter(user=request.user).order_by('-date')
        
        # Apply filters
        activity_type = request.GET.get('activity_type')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if activity_type and activity_type in dict(Activity.ACTIVITY_TYPES):
            activities = activities.filter(activity_type=activity_type)
        if start_date:
            try:
                activities = activities.filter(date__date__gte=start_date)
            except ValueError:
                messages.error(request, 'Invalid start date format.')
        if end_date:
            try:
                activities = activities.filter(date__date__lte=end_date)
            except ValueError:
                messages.error(request, 'Invalid end date format.')
        
        # Pagination
        paginator = Paginator(activities, 12)  # 12 activities per page
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.get_page(page_number)
        except Exception:
            page_obj = paginator.get_page(1)
        
        context = {
            'activities': page_obj,
            'activity_types': Activity.ACTIVITY_TYPES,
        }
    except Exception as e:
        messages.error(request, 'Error loading activities. Please try again.')
        context = {'activities': [], 'activity_types': Activity.ACTIVITY_TYPES}
    
    return render(request, 'activities.html', context)

@login_required
@csrf_protect
def add_activity_view(request):
    """Add new activity view"""
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            try:
                activity = form.save(commit=False)
                activity.user = request.user
                activity.save()
                messages.success(request, 'Activity added successfully!')
                return redirect('activities')
            except Exception as e:
                messages.error(request, 'Error saving activity. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ActivityForm()
    
    return render(request, 'add_activity.html', {'form': form})

@login_required
def profile_view(request):
    """User profile view"""
    try:
        activities = Activity.objects.filter(user=request.user).order_by('-date')
        
        # Calculate profile statistics
        total_activities = activities.count()
        total_duration = activities.aggregate(Sum('duration'))['duration__sum'] or 0
        total_distance = activities.aggregate(Sum('distance'))['distance__sum'] or 0
        total_calories = activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        avg_duration = activities.aggregate(Avg('duration'))['duration__avg'] or 0
        
        # Get activity type distribution
        activity_distribution = activities.values('activity_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Get monthly progress (last 6 months)
        monthly_data = []
        for i in range(6):
            try:
                month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30*i)
                month_end = month_start.replace(day=28) + timedelta(days=4)
                month_end = month_end.replace(day=1) - timedelta(days=1)
                
                month_activities = activities.filter(date__range=[month_start, month_end])
                month_duration = month_activities.aggregate(Sum('duration'))['duration__sum'] or 0
                
                monthly_data.append({
                    'month': month_start.strftime('%B %Y'),
                    'duration': month_duration
                })
            except Exception:
                continue
        
        monthly_data.reverse()
        
        context = {
            'user': request.user,
            'total_activities': total_activities,
            'total_duration': total_duration,
            'total_distance': total_distance,
            'total_calories': total_calories,
            'avg_duration': round(avg_duration, 1) if avg_duration else 0,
            'activity_distribution': activity_distribution,
            'monthly_data': monthly_data,
        }
    except Exception as e:
        messages.error(request, 'Error loading profile data. Please try again.')
        context = {
            'user': request.user,
            'total_activities': 0,
            'total_duration': 0,
            'total_distance': 0,
            'total_calories': 0,
            'avg_duration': 0,
            'activity_distribution': [],
            'monthly_data': [],
        }
    
    return render(request, 'profile.html', context)

def debug_static_view(request):
    """Debug view to test static file serving"""
    return render(request, 'debug_static.html')
