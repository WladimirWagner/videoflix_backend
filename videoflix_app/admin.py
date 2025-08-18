from django.contrib import admin
from .models import Profile, Video

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['username__username', 'email']
    readonly_fields = ['created_at']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']

# Register your models here.
