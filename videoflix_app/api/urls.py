from django.urls import path
from . import views

urlpatterns = [
    path('video/', views.VideoView.as_view(), name='video'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', views.HLSManifestView.as_view(), name='hls-manifest'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', views.HLSSegmentView.as_view(), name='hls-segment'),
]