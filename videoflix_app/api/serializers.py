from rest_framework import serializers
from videoflix_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for Video model.
    Returns video metadata exactly as specified in API documentation.
    """
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']
        read_only_fields = ['id', 'created_at']
    
    def get_thumbnail_url(self, obj):
        """Return thumbnail URL from computed property"""
        return obj.thumbnail_url_computed
