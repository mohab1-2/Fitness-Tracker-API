from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Activity
from .serializers import UserRegistrationSerializer, ActivitySerializer, ActivityMetricsSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        
        # Optional filters for activity history
        date_range = self.request.query_params.get('date_range', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if date_range:
            if date_range == 'week':
                start_date = timezone.now().date() - timedelta(days=7)
                queryset = queryset.filter(date__gte=start_date)
            elif date_range == 'month':
                start_date = timezone.now().date() - timedelta(days=30)
                queryset = queryset.filter(date__gte=start_date)
        
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_history(request):
    """
    Endpoint to view activity history with optional filters
    """
    activities = Activity.objects.filter(user=request.user)
    
    # Apply filters
    date_range = request.query_params.get('date_range', None)
    activity_type = request.query_params.get('activity_type', None)
    
    if date_range:
        if date_range == 'week':
            start_date = timezone.now().date() - timedelta(days=7)
            activities = activities.filter(date__gte=start_date)
        elif date_range == 'month':
            start_date = timezone.now().date() - timedelta(days=30)
            activities = activities.filter(date__gte=start_date)
    
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    serializer = ActivitySerializer(activities, many=True)
    return Response({
        'activities': serializer.data,
        'total_activities': activities.count()
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_metrics(request):
    """
    Endpoint to get activity metrics summary
    """
    period = request.query_params.get('period', 'all')
    activities = Activity.objects.filter(user=request.user)
    
    # Filter by period
    if period == 'week':
        start_date = timezone.now().date() - timedelta(days=7)
        activities = activities.filter(date__gte=start_date)
        period_label = 'Last 7 days'
    elif period == 'month':
        start_date = timezone.now().date() - timedelta(days=30)
        activities = activities.filter(date__gte=start_date)
        period_label = 'Last 30 days'
    else:
        period_label = 'All time'
    
    # Calculate metrics
    metrics = activities.aggregate(
        total_duration=Sum('duration'),
        total_distance=Sum('distance'),
        total_calories_burned=Sum('calories_burned'),
        activity_count=Count('id')
    )
    
    # Handle None values
    for key, value in metrics.items():
        if value is None:
            metrics[key] = 0
    
    metrics['period'] = period_label
    
    serializer = ActivityMetricsSerializer(metrics)
    return Response(serializer.data)