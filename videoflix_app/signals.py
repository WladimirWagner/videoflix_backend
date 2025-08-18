# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from videoflix_app.models import Video
# from videoflix_app.tasks import convert_480p, convert_720p
# import django_rq

# @receiver(post_save, sender=Video)
# def video_post_save(sender, instance, created, **kwargs):
#     if created:
#         instance.generate_thumbnail()
#         instance.generate_preview()
#         instance.generate_video_info()
#         instance.generate_video_info()
#         queue = django_rq.get_queue('default', autocommit=True)
#         queue.enqueue(convert_480p, instance.video_file.path)
#         queue.enqueue(convert_720p, instance.video_file.path)

# @receiver(post_delete, sender=Video)
# def video_post_delete(sender, instance, **kwargs):
#     if instance.video_file:
#         instance.video_file.delete(save=False)
#     if instance.thumbnail_image:
#         instance.thumbnail_image.delete(save=False)
#     if instance.preview_image:
#         instance.preview_image.delete(save=False)

