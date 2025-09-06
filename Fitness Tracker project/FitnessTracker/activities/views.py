from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from django.db.models import Sum, Count
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from .models import User, Activity
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    ActivitySerializer,
    ActivityCreateUpdateSerializer,
    ActivitySummarySerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': 'Registration failed. Please try again.'},
                status=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(csrf_exempt, name='dispatch')
class CustomAuthToken(ObtainAuthToken):
    """Custom authentication token view"""
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            if username and password:
                user = authenticate(username=username, password=password)
                if user and user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user': UserSerializer(user).data
                    })
            
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {'error': 'Authentication failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ActivityListCreateView(generics.ListCreateAPIView):
    """List and create activities for authenticated user"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ActivityCreateUpdateSerializer
        return ActivitySerializer
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            raise serializers.ValidationError('Error creating activity. Please try again.')


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete specific activity"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ActivityCreateUpdateSerializer
        return ActivitySerializer
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)


class ActivityHistoryView(generics.ListAPIView):
    """View activity history with optional filters"""
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        
        try:
            # Filter by date range
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            
            if start_date:
                start_date = parse_date(start_date)
                if start_date:
                    queryset = queryset.filter(date__gte=start_date)
            
            if end_date:
                end_date = parse_date(end_date)
                if end_date:
                    queryset = queryset.filter(date__lte=end_date)
            
            # Filter by activity type
            activity_type = self.request.query_params.get('activity_type')
            if activity_type and activity_type in dict(Activity.ACTIVITY_TYPES):
                queryset = queryset.filter(activity_type=activity_type)
        except Exception:
            pass  # Return unfiltered queryset if filtering fails
        
        return queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_metrics(request):
    """Get activity metrics/summary for the user"""
    try:
        user = request.user
        
        # Get date range from query params (default to last 30 days)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        start_param = request.query_params.get('start_date')
        end_param = request.query_params.get('end_date')
        
        if start_param:
            parsed_start = parse_date(start_param)
            if parsed_start:
                start_date = parsed_start
        if end_param:
            parsed_end = parse_date(end_param)
            if parsed_end:
                end_date = parsed_end
        
        # Get activities in date range
        activities = Activity.objects.filter(
            user=user,
            date__date__gte=start_date,
            date__date__lte=end_date
        )
        
        # Calculate metrics
        metrics = activities.aggregate(
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_calories_burned=Sum('calories_burned'),
            activity_count=Count('id')
        )
        
        # Handle None values
        metrics['total_duration'] = metrics['total_duration'] or 0
        metrics['total_distance'] = metrics['total_distance'] or 0
        metrics['total_calories_burned'] = metrics['total_calories_burned'] or 0
        metrics['date_range'] = f"{start_date} to {end_date}"
        
        serializer = ActivitySummarySerializer(metrics)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Error calculating metrics'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_trends(request):
    """Get activity trends over time (optional feature)"""
    try:
        user = request.user
        
        # Get weekly trends for the last 12 weeks
        end_date = datetime.now().date()
        start_date = end_date - timedelta(weeks=12)
        
        activities = Activity.objects.filter(
            user=user,
            date__date__gte=start_date,
            date__date__lte=end_date
        )
        
        # Group by week and calculate totals
        weekly_data = []
        current_date = start_date
        
        while current_date <= end_date:
            week_end = current_date + timedelta(days=6)
            week_activities = activities.filter(
                date__date__gte=current_date,
                date__date__lte=week_end
            )
            
            week_metrics = week_activities.aggregate(
                total_duration=Sum('duration'),
                total_distance=Sum('distance'),
                total_calories_burned=Sum('calories_burned'),
                activity_count=Count('id')
            )
            
            # Handle None values
            week_metrics['total_duration'] = week_metrics['total_duration'] or 0
            week_metrics['total_distance'] = week_metrics['total_distance'] or 0
            week_metrics['total_calories_burned'] = week_metrics['total_calories_burned'] or 0
            week_metrics['week_start'] = current_date.strftime('%Y-%m-%d')
            weekly_data.append(week_metrics)
            
            current_date += timedelta(days=7)
        
        return Response({'weekly_trends': weekly_data})
    except Exception as e:
        return Response(
            {'error': 'Error calculating trends'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )