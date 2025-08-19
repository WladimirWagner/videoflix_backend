from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from videoflix_app.models import Video
from videoflix_app.tasks import convert_video_to_hls, generate_thumbnail
import django_rq
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Process video when it's created or when video_file is added
    """
    if created and instance.video_file:
        logger.info(f"New video created: {instance.title} (ID: {instance.id})")
        
        try:
            queue = django_rq.get_queue('default')
            
            queue.enqueue(generate_thumbnail, instance.id)
            
            queue.enqueue(convert_video_to_hls, instance.id)
        except Exception as e:
            logger.error(f"Failed to queue tasks for video {instance.id}: {e}")
        
        logger.info(f"Queued processing tasks for video {instance.id}")
    
    elif not created and instance.video_file and not instance.is_processing and not instance.processing_complete:
        logger.info(f"Video file added to existing video: {instance.title} (ID: {instance.id})")
        
        try:
            queue = django_rq.get_queue('default')
            queue.enqueue(generate_thumbnail, instance.id)
            queue.enqueue(convert_video_to_hls, instance.id)
        except Exception as e:
            logger.error(f"Failed to queue tasks for existing video {instance.id}: {e}")

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Clean up files when video is deleted
    """
    import os
    from django.conf import settings
    
    logger.info(f"Deleting video: {instance.title} (ID: {instance.id})")
    
    if instance.video_file:
        try:
            instance.video_file.delete(save=False)
        except Exception as e:
            logger.error(f"Error deleting video file: {e}")
    
    if instance.thumbnail_image:
        try:
            instance.thumbnail_image.delete(save=False)
        except Exception as e:
            logger.error(f"Error deleting thumbnail: {e}")
    
    if instance.preview_image:
        try:
            instance.preview_image.delete(save=False)
        except Exception as e:
            logger.error(f"Error deleting preview: {e}")
    
    if instance.hls_path:
        try:
            hls_dir = os.path.join(settings.MEDIA_ROOT, instance.hls_path)
            if os.path.exists(hls_dir):
                import shutil
                shutil.rmtree(hls_dir)
                logger.info(f"Deleted HLS directory: {hls_dir}")
        except Exception as e:
            logger.error(f"Error deleting HLS files: {e}")

