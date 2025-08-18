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
        
        # Queue background tasks
        queue = django_rq.get_queue('default', autocommit=True)
        
        # Generate thumbnail first
        queue.enqueue(generate_thumbnail, instance.id)
        
        # Then convert to HLS
        queue.enqueue(convert_video_to_hls, instance.id)
        
        logger.info(f"Queued processing tasks for video {instance.id}")
    
    elif not created and instance.video_file and not instance.is_processing and not instance.processing_complete:
        # Video file was added to existing video
        logger.info(f"Video file added to existing video: {instance.title} (ID: {instance.id})")
        
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(generate_thumbnail, instance.id)
        queue.enqueue(convert_video_to_hls, instance.id)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Clean up files when video is deleted
    """
    import os
    from django.conf import settings
    
    logger.info(f"Deleting video: {instance.title} (ID: {instance.id})")
    
    # Delete original video file
    if instance.video_file:
        try:
            instance.video_file.delete(save=False)
        except Exception as e:
            logger.error(f"Error deleting video file: {e}")
    
    # Delete thumbnail
    if instance.thumbnail_image:
        try:
            instance.thumbnail_image.delete(save=False)
        except Exception as e:
            logger.error(f"Error deleting thumbnail: {e}")
    
    # Delete preview image
    if instance.preview_image:
        try:
            instance.preview_image.delete(save=False)
        except Exception as e:
            logger.error(f"Error deleting preview: {e}")
    
    # Delete HLS files
    if instance.hls_path:
        try:
            hls_dir = os.path.join(settings.MEDIA_ROOT, instance.hls_path)
            if os.path.exists(hls_dir):
                import shutil
                shutil.rmtree(hls_dir)
                logger.info(f"Deleted HLS directory: {hls_dir}")
        except Exception as e:
            logger.error(f"Error deleting HLS files: {e}")

