from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Weightlifting', 'Weightlifting'),
        ('Swimming', 'Swimming'),
        ('Walking', 'Walking'),
        ('Yoga', 'Yoga'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Duration in minutes")
    distance = models.FloatField(validators=[MinValueValidator(0.1)], help_text="Distance in km or miles")
    calories_burned = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    date = models.DateField()
    user_id = models.PositiveIntegerField(editable=False)
    
    class Meta:
        ordering = ['-date', '-id']
    
    def save(self, *args, **kwargs):
        self.user_id = self.user.id
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"