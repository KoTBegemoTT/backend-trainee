import rest_framework.serializers
from rest_framework.serializers import ModelSerializer
from .models import Banner


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class UserBannerQuerySerializer(ModelSerializer):
    feature_id = rest_framework.serializers.IntegerField()
    tag_id = rest_framework.serializers.IntegerField()
    use_last_revision = rest_framework.serializers.BooleanField(required=False)

    class Meta:
        model = Banner
        fields = ['feature_id', 'tag_id', 'use_last_revision']
