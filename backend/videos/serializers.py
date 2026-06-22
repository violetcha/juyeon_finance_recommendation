from rest_framework import serializers
from .models import SavedVideo


class SavedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedVideo
        fields = [
            'id',
            'video_id',
            'title',
            'channel_title',
            'channel_id',
            'description',
            'thumbnail_url',
            'published_at',
            'saved_at',
        ]
        read_only_fields = ['id', 'saved_at']