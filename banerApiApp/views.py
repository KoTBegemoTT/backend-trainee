from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer


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
def get_banner(request, banner_id):
    # Todo change this view on user_banner
    try:
        banner = Banner.objects.get(banner_id=banner_id)
        serializer = BannerSerializer(banner)
        return Response(serializer.data)
    except Banner.DoesNotExist:
        return Response("Banner not found", status=404)


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
