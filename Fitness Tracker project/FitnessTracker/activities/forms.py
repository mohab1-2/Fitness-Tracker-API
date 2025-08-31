from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Activity

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form that works with the custom User model"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_type', 'duration', 'distance', 'calories_burned', 'date']
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-input'}),
            'duration': forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'max': '1440'}),
            'distance': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '0.1'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
        }
    
    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration and (duration < 1 or duration > 1440):
            raise forms.ValidationError('Duration must be between 1 and 1440 minutes.')
        return duration
    
    def clean_distance(self):
        distance = self.cleaned_data.get('distance')
        if distance and distance < 0:
            raise forms.ValidationError('Distance cannot be negative.')
        return distance
    
    def clean_calories_burned(self):
        calories = self.cleaned_data.get('calories_burned')
        if calories and calories < 0:
            raise forms.ValidationError('Calories cannot be negative.')
        return calories
