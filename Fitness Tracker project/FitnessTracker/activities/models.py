from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with additional fields"""
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Activity(models.Model):
    """Model for fitness activities"""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('weightlifting', 'Weightlifting'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('yoga', 'Yoga'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Duration in minutes"
    )
    distance = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Distance in km or miles"
    )
    calories_burned = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Calories burned during the activity"
    )
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date.strftime('%Y-%m-%d')}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.duration and (self.duration < 1 or self.duration > 1440):
            raise ValidationError('Duration must be between 1 and 1440 minutes.')
        if self.distance and self.distance < 0:
            raise ValidationError('Distance cannot be negative.')
        if self.calories_burned and self.calories_burned < 0:
            raise ValidationError('Calories burned cannot be negative.')