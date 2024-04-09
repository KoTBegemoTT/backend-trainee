from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Banner


class ContentSerializer(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField()
    url = serializers.URLField()


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ['banner_id', 'tag_ids', 'feature_id', 'content', 'is_active', 'created_at', 'updated_at']
