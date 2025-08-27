from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Activity
from datetime import date

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'activity_type', 'duration', 'distance', 'calories_burned', 'date', 'user_id')
        read_only_fields = ('id', 'user_id')
    
    def validate_activity_type(self, value):
        if not value:
            raise serializers.ValidationError("Activity type is required.")
        return value
    
    def validate_duration(self, value):
        if not value or value <= 0:
            raise serializers.ValidationError("Duration must be a positive number.")
        return value
    
    def validate_date(self, value):
        if not value:
            raise serializers.ValidationError("Date is required.")
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

class ActivityMetricsSerializer(serializers.Serializer):
    total_duration = serializers.IntegerField()
    total_distance = serializers.FloatField()
    total_calories_burned = serializers.IntegerField()
    activity_count = serializers.IntegerField()
    period = serializers.CharField()
