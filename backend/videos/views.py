import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import SavedVideo
from .serializers import SavedVideoSerializer


YOUTUBE_BASE_URL = 'https://www.googleapis.com/youtube/v3'


@api_view(['GET'])
@permission_classes([AllowAny])
def youtube_search(request):
    keyword = request.GET.get('q', '주거래은행 선택 기준')
    max_results = request.GET.get('max_results', 3)

    if not settings.YOUTUBE_API_KEY:
        return Response(
            {'message': 'YOUTUBE_API_KEY가 설정되지 않았습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        response = requests.get(
            f'{YOUTUBE_BASE_URL}/search',
            params={
                'key': settings.YOUTUBE_API_KEY,
                'part': 'snippet',
                'q': keyword,
                'type': 'video',
                'maxResults': max_results,
                'order': 'relevance',
            },
            timeout=5,
        )

        if response.status_code != 200:
            try:
                youtube_error = response.json()
            except ValueError:
                youtube_error = response.text

            return Response(
                {
                    'message': 'YouTube API 요청 중 오류가 발생했습니다.',
                    'youtube_status_code': response.status_code,
                    'youtube_error': youtube_error,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except requests.RequestException as error:
        return Response(
            {
                'message': 'YouTube API 요청 중 네트워크 오류가 발생했습니다.',
                'error': str(error),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    items = response.json().get('items', [])
    videos = []

    for item in items:
        snippet = item.get('snippet', {})
        thumbnails = snippet.get('thumbnails', {})
        video_id = item.get('id', {}).get('videoId')

        if not video_id:
            continue

        videos.append({
            'video_id': video_id,
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'channel_title': snippet.get('channelTitle', ''),
            'channel_id': snippet.get('channelId', ''),
            'published_at': snippet.get('publishedAt'),
            'thumbnail_url': (
                thumbnails.get('medium', {}).get('url')
                or thumbnails.get('default', {}).get('url')
                or ''
            ),
        })

    return Response(videos)


@api_view(['GET'])
@permission_classes([AllowAny])
def youtube_detail(request, video_id):
    if not settings.YOUTUBE_API_KEY:
        return Response(
            {'message': 'YOUTUBE_API_KEY가 설정되지 않았습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        response = requests.get(
            f'{YOUTUBE_BASE_URL}/videos',
            params={
                'key': settings.YOUTUBE_API_KEY,
                'part': 'snippet,statistics',
                'id': video_id,
            },
            timeout=5,
        )

        if response.status_code != 200:
            try:
                youtube_error = response.json()
            except ValueError:
                youtube_error = response.text

            return Response(
                {
                    'message': 'YouTube API 요청 중 오류가 발생했습니다.',
                    'youtube_status_code': response.status_code,
                    'youtube_error': youtube_error,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except requests.RequestException as error:
        return Response(
            {
                'message': 'YouTube API 요청 중 네트워크 오류가 발생했습니다.',
                'error': str(error),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    items = response.json().get('items', [])

    if not items:
        return Response(
            {'message': '영상을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    item = items[0]
    snippet = item.get('snippet', {})
    statistics = item.get('statistics', {})
    thumbnails = snippet.get('thumbnails', {})

    video = {
        'video_id': item.get('id'),
        'title': snippet.get('title', ''),
        'description': snippet.get('description', ''),
        'channel_title': snippet.get('channelTitle', ''),
        'channel_id': snippet.get('channelId', ''),
        'published_at': snippet.get('publishedAt'),
        'thumbnail_url': (
            thumbnails.get('medium', {}).get('url')
            or thumbnails.get('default', {}).get('url')
            or ''
        ),
        'view_count': statistics.get('viewCount'),
    }

    return Response(video)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def saved_video_list_create(request):
    if request.method == 'GET':
        videos = SavedVideo.objects.filter(user=request.user)
        serializer = SavedVideoSerializer(videos, many=True)
        return Response(serializer.data)

    serializer = SavedVideoSerializer(data=request.data)

    if serializer.is_valid():
        video, created = SavedVideo.objects.get_or_create(
            user=request.user,
            video_id=serializer.validated_data['video_id'],
            defaults={
                'title': serializer.validated_data.get('title', ''),
                'channel_title': serializer.validated_data.get('channel_title', ''),
                'channel_id': serializer.validated_data.get('channel_id', ''),
                'description': serializer.validated_data.get('description', ''),
                'thumbnail_url': serializer.validated_data.get('thumbnail_url', ''),
                'published_at': serializer.validated_data.get('published_at'),
            }
        )

        result_serializer = SavedVideoSerializer(video)

        if created:
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {
                'message': '이미 저장된 영상입니다.',
                'video': result_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def saved_video_delete(request, video_id):
    try:
        video = SavedVideo.objects.get(user=request.user, video_id=video_id)
    except SavedVideo.DoesNotExist:
        return Response(
            {'message': '저장된 영상을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    video.delete()
    return Response({'message': '저장한 영상을 삭제했습니다.'})