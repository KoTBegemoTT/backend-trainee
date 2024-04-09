from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Banner
from .serializers import BannerSerializer, ContentSerializer
import json


@api_view(["GET"])
def index(request):
    return Response({"Success": "The setup was successful"})


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
        banner = Banner.objects.filter(is_active=True).filter(feature_id=feature_id).get(tag_ids=tag_id)
        return Response(banner.content)
    except Banner.DoesNotExist:
        return Response(status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


def get_query_params(request):
    feature_id = request.query_params.get('feature_id', None)
    if feature_id is not None:
        feature_id = int(feature_id)
    tag_id = request.query_params.get('tag_id', None)
    if tag_id is not None:
        tag_id = int(tag_id)
    limit = request.query_params.get('limit', None)
    if limit is not None:
        limit = int(limit)
    offset = request.query_params.get('offset', None)
    if offset is not None:
        offset = int(offset)

    if limit is not None and limit < 0:
        raise ValueError('Limit must be non negative')
    if offset is not None and offset < 0:
        raise ValueError('Offset must be non negative')

    return feature_id, tag_id, limit, offset


def found_banners(feature_id, tag_id, limit, offset):
    banners = Banner.objects.all()
    if feature_id is not None:
        banners = banners.filter(feature_id=feature_id)
    if tag_id is not None:
        banners = banners.filter(tag_ids=tag_id)

    if limit is not None:
        banners = banners[:limit + 1]
    if offset is not None:
        banners = banners[offset:]

    return banners


@api_view(["GET", 'POST'])
def banner_view(request):
    """
    List all banners snippets, or create a new banner.
    """
    if request.method == 'GET':
        try:
            feature_id, tag_id, limit, offset = get_query_params(request)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        try:
            banners = found_banners(feature_id, tag_id, limit, offset)
            serializer = BannerSerializer(banners, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    elif request.method == 'POST':
        data = request.data
        banner_serializer = BannerSerializer(data=data)

        try:
            banner_serializer.is_valid(raise_exception=True)
            content_serializer = ContentSerializer(data=json.loads(data.get('content')))
            content_serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        try:
            banner_serializer.save()
            return Response({"banner_id": banner_serializer.data.get('banner_id')}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


@api_view(["PATCH", 'DELETE'])
def update_banner(request, banner_id: str):
    """
    Patch banner or delete by id
    """
    try:
        banner = Banner.objects.get(banner_id=banner_id)
    except Banner.DoesNotExist:
        return Response(status=404)

    if request.method == 'PATCH':
        banner_serializer = BannerSerializer(banner, data=request.data, partial=True)
        try:
            banner_serializer.is_valid(raise_exception=True)
            if 'content' in request.data:
                content_serializer = ContentSerializer(data=json.loads(request.data.get('content')))
                content_serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        try:
            banner_serializer.save()
            return Response(status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            banner.delete()
            return Response("Banner deleted successfully", status=204)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
