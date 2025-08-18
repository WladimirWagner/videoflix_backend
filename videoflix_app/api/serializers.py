from rest_framework import serializers
from videoflix_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for Video model.
    Returns video metadata including id, created_at, title, description, thumbnail_url, and category.
    """
    
    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']
        read_only_fields = ['id', 'created_at']
