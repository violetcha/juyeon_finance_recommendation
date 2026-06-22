from django.conf import settings
from django.db import models


class SavedVideo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_videos'
    )
    video_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    channel_title = models.CharField(max_length=255, blank=True)
    channel_id = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video_id')
        ordering = ['-saved_at']

    def __str__(self):
        return f'{self.user} - {self.title}'