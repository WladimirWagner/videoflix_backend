from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """User profile model for additional user information"""
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    """Video model for storing video information"""
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField()
    category = models.CharField(max_length=255)
    hls_path = models.CharField(max_length=500, blank=True, null=True)  # Path to HLS files
    
    def __str__(self):
        return self.title