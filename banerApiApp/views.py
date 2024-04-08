import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer, UserBannerQuerySerializer


# Create your views here.

@api_view(["GET"])
def index(request):
    return Response({"Success": "The setup was successful"})


@api_view(["GET", 'POST'])
def banner_view(request):
    """
    List all banners snippets, or create a new banner.
    """
    if request.method == 'GET':
        banners = Banner.objects.all()
        serialized_banners = BannerSerializer(banners, many=True)
        return Response(serialized_banners.data)

    elif request.method == 'POST':
        data = request.data
        serializer = BannerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Banner added successfully", status=201)
        else:
            return Response(serializer.errors, status=400)


@api_view(["GET"])
def get_banner(request):
    try:
        tag_id = int(request.query_params.get('tag_id'))
        feature_id = int(request.query_params.get('feature_id'))
        use_last_version = bool(request.query_params.get('use_last_revision', False))
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    # Todo add use_last_version
    try:
        banner = Banner.objects.filter(feature_id=feature_id).get(tag_ids=tag_id)
        serializer = BannerSerializer(banner)
    except Banner.DoesNotExist:
        return Response(status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    return Response(serializer.data)


@api_view(["PATCH", 'DELETE'])
def update_banner(request, banner_id):
    """
    Patch banner or delete by id
    """
    if request.method == 'PATCH':
        try:
            banner = Banner.objects.get(banner_id=banner_id)
            serializer = BannerSerializer(banner, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response("Banner updated successfully", status=200)
            else:
                return Response(serializer.errors, status=400)
        except Banner.DoesNotExist:
            return Response("Banner not found", status=404)

    elif request.method == 'DELETE':
        try:
            banner = Banner.objects.get(banner_id=banner_id)
            banner.delete()
            return Response("Banner deleted successfully", status=200)
        except Banner.DoesNotExist:
            return Response("Banner not found", status=404)
