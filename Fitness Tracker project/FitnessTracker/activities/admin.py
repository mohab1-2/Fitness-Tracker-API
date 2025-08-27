from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date')
    list_filter = ('activity_type', 'date', 'user')
    search_fields = ('user__username', 'activity_type')
    readonly_fields = ('user_id',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
