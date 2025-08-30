from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Activity


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'activity_type', 'duration', 'distance', 
            'calories_burned', 'date', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive")
        return value

    def validate_distance(self, value):
        if value < 0:
            raise serializers.ValidationError("Distance cannot be negative")
        return value

    def validate_calories_burned(self, value):
        if value < 0:
            raise serializers.ValidationError("Calories burned cannot be negative")
        return value


class ActivityCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating activities"""
    class Meta:
        model = Activity
        fields = ['activity_type', 'duration', 'distance', 'calories_burned', 'date']

    def create(self, validated_data):
        # The user will be set in the view
        return Activity.objects.create(**validated_data)


class ActivitySummarySerializer(serializers.Serializer):
    """Serializer for activity metrics/summary"""
    total_duration = serializers.IntegerField()
    total_distance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_calories_burned = serializers.IntegerField()
    activity_count = serializers.IntegerField()
    date_range = serializers.CharField()