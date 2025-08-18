from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """User profile model for additional user information"""
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

import os
from django.conf import settings

class Video(models.Model):
    """Video model for storing video information and processing"""
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    
    video_file = models.FileField(upload_to='videos/originals/', blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    preview_image = models.ImageField(upload_to='videos/previews/', blank=True, null=True)
    
    hls_path = models.CharField(max_length=500, blank=True, null=True)
    is_processing = models.BooleanField(default=False)
    processing_complete = models.BooleanField(default=False)
    
    has_480p = models.BooleanField(default=False)
    has_720p = models.BooleanField(default=False)
    has_1080p = models.BooleanField(default=False)
    
    thumbnail_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    @property
    def thumbnail_url_computed(self):
        """Return thumbnail URL - either from file or URL field"""
        if self.thumbnail_image:
            return self.thumbnail_image.url
        return self.thumbnail_url or ''
    
    def get_available_resolutions(self):
        """Return list of available resolutions"""
        resolutions = []
        if self.has_480p:
            resolutions.append('480p')
        if self.has_720p:
            resolutions.append('720p')
        if self.has_1080p:
            resolutions.append('1080p')
        return resolutions