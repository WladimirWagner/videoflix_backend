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
        """Return absolute thumbnail URL for cross-origin requests"""
        if obj.thumbnail_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail_image.url)
            else:
                return f"http://127.0.0.1:8000{obj.thumbnail_image.url}"
        return obj.thumbnail_url or ''
