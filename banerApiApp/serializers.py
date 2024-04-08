import rest_framework.serializers
from rest_framework.serializers import ModelSerializer
from .models import Banner


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class UserBannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'text', 'url']
