from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404
from django.conf import settings
from .serializers import VideoSerializer
from videoflix_app.models import Video
import os

class VideoView(APIView):
    """
    Handles video listing endpoint.
    Returns all available videos with metadata.
    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            videos = Video.objects.all().order_by('-created_at')
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HLSManifestView(APIView):
    """
    Handles HLS manifest delivery for video streaming.
    Returns M3U8 playlist files for specified video and resolution.
    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        try:
            # Get the video object
            video = Video.objects.get(id=movie_id)
            
            # Construct the HLS manifest file path
            if video.hls_path:
                manifest_path = os.path.join(
                    settings.MEDIA_ROOT, 
                    video.hls_path, 
                    resolution, 
                    'index.m3u8'
                )
            else:
                # Fallback path structure
                manifest_path = os.path.join(
                    settings.MEDIA_ROOT, 
                    'videos', 
                    f'video_{movie_id}', 
                    resolution, 
                    'index.m3u8'
                )
            
            # Check if the manifest file exists
            if not os.path.exists(manifest_path):
                return Response(
                    {'error': 'Video manifest not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Read and return the M3U8 file
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_content = f.read()
            
            return HttpResponse(
                manifest_content,
                content_type='application/vnd.apple.mpegurl'
            )
            
        except Video.DoesNotExist:
            return Response(
                {'error': 'Video not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HLSSegmentView(APIView):
    """
    Handles HLS segment delivery for video streaming.
    Returns TS segment files for specified video, resolution and segment.
    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        try:
            # Get the video object
            video = Video.objects.get(id=movie_id)
            
            # Construct the segment file path
            if video.hls_path:
                segment_path = os.path.join(
                    settings.MEDIA_ROOT, 
                    video.hls_path, 
                    resolution, 
                    segment
                )
            else:
                # Fallback path structure
                segment_path = os.path.join(
                    settings.MEDIA_ROOT, 
                    'videos', 
                    f'video_{movie_id}', 
                    resolution, 
                    segment
                )
            
            # Check if the segment file exists
            if not os.path.exists(segment_path):
                return Response(
                    {'error': 'Video segment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Read and return the TS segment file
            with open(segment_path, 'rb') as f:
                segment_content = f.read()
            
            return HttpResponse(
                segment_content,
                content_type='video/MP2T'
            )
            
        except Video.DoesNotExist:
            return Response(
                {'error': 'Video not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
