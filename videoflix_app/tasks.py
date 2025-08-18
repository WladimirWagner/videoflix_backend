import os
import subprocess
from django.conf import settings
from videoflix_app.models import Video
import logging

logger = logging.getLogger(__name__)

def convert_video_to_hls(video_id):
    """
    Convert video to HLS format with multiple resolutions
    This runs as a background task
    """
    try:
        video = Video.objects.get(id=video_id)
        if not video.video_file:
            logger.error(f"No video file found for video {video_id}")
            return
        
        video.is_processing = True
        video.save()
        
        video_name = os.path.splitext(os.path.basename(video.video_file.name))[0]
        output_dir = os.path.join(settings.MEDIA_ROOT, 'videos', 'hls', f'video_{video_id}')
        os.makedirs(output_dir, exist_ok=True)
        
        input_path = video.video_file.path
        
        resolutions = [
            {'name': '480p', 'scale': '854:480', 'bitrate': '800k'},
            {'name': '720p', 'scale': '1280:720', 'bitrate': '2500k'},
            {'name': '1080p', 'scale': '1920:1080', 'bitrate': '5000k'}
        ]
        
        for res in resolutions:
            try:
                output_path = os.path.join(output_dir, res['name'])
                os.makedirs(output_path, exist_ok=True)
                
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-vf', f"scale={res['scale']}",
                    '-c:v', 'libx264',
                    '-b:v', res['bitrate'],
                    '-c:a', 'aac',
                    '-hls_time', '6',
                    '-hls_playlist_type', 'vod',
                    '-hls_segment_filename', os.path.join(output_path, 'segment_%03d.ts'),
                    os.path.join(output_path, 'index.m3u8')
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    if res['name'] == '480p':
                        video.has_480p = True
                    elif res['name'] == '720p':
                        video.has_720p = True
                    elif res['name'] == '1080p':
                        video.has_1080p = True
                    
                    logger.info(f"Successfully converted {res['name']} for video {video_id}")
                else:
                    logger.error(f"FFmpeg error for {res['name']}: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Error converting {res['name']} for video {video_id}: {e}")
        
        video.hls_path = f'videos/hls/video_{video_id}'
        video.is_processing = False
        video.processing_complete = True
        video.save()
        
        logger.info(f"Video processing completed for video {video_id}")
        
    except Video.DoesNotExist:
        logger.error(f"Video {video_id} not found")
    except Exception as e:
        logger.error(f"Error processing video {video_id}: {e}")
        try:
            video = Video.objects.get(id=video_id)
            video.is_processing = False
            video.save()
        except:
            pass

def generate_thumbnail(video_id):
    """Generate thumbnail for video"""
    try:
        video = Video.objects.get(id=video_id)
        if not video.video_file:
            return
        
        input_path = video.video_file.path
        thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'videos', 'thumbnails')
        os.makedirs(thumbnail_dir, exist_ok=True)
        
        thumbnail_path = os.path.join(thumbnail_dir, f'video_{video_id}_thumb.jpg')
        
        cmd = [
            'ffmpeg', '-i', input_path,
            '-ss', '00:00:10', 
            '-vframes', '1',
            '-vf', 'scale=640:360',
            thumbnail_path, '-y'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            relative_path = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT)
            video.thumbnail_image = relative_path
            video.save()
            logger.info(f"Thumbnail generated for video {video_id}")
        else:
            logger.error(f"Thumbnail generation failed for video {video_id}: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Error generating thumbnail for video {video_id}: {e}")
