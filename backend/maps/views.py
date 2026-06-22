import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])
def bank_search(request):
    # 프론트에서 bank=국민은행 으로 보내고 있으므로 bank를 받아야 함
    bank = request.GET.get('bank', '은행')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    if not lat or not lng:
        return Response(
            {'message': 'lat, lng 값이 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not settings.KAKAO_REST_API_KEY:
        return Response(
            {'message': 'KAKAO_REST_API_KEY가 설정되지 않았습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_REST_API_KEY}'
    }

    # 중요:
    # Kakao Local API에서 x = 경도(lng), y = 위도(lat)
    params = {
        'query': bank,
        'x': lng,
        'y': lat,
        'radius': 5000,
        'sort': 'distance',
        'size': 15,
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=5
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print('Kakao bank search error:', error)
        return Response(
            {'message': '카카오 은행 검색 중 오류가 발생했습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    documents = response.json().get('documents', [])

    branches = []

    for item in documents:
        branches.append({
            'id': item.get('id'),
            'place_name': item.get('place_name'),
            'address_name': item.get('address_name'),
            'road_address_name': item.get('road_address_name'),
            'phone': item.get('phone'),
            'x': item.get('x'),  # 경도
            'y': item.get('y'),  # 위도
            'distance': item.get('distance'),
            'place_url': item.get('place_url'),
        })

    return Response({
        'keyword': bank,
        'lat': lat,
        'lng': lng,
        'count': len(branches),
        'branches': branches,
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def route_search(request):
    origin_lat = request.GET.get('origin_lat')
    origin_lng = request.GET.get('origin_lng')
    destination_lat = request.GET.get('destination_lat')
    destination_lng = request.GET.get('destination_lng')
    priority = request.GET.get('priority', 'RECOMMEND')

    if not all([origin_lat, origin_lng, destination_lat, destination_lng]):
        return Response(
            {'message': 'origin_lat, origin_lng, destination_lat, destination_lng 값이 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not settings.KAKAO_REST_API_KEY:
        return Response(
            {'message': 'KAKAO_REST_API_KEY가 설정되지 않았습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    url = 'https://apis-navi.kakaomobility.com/v1/directions'

    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_REST_API_KEY}',
        'Content-Type': 'application/json',
    }

    # Kakao Mobility도 origin/destination은 경도,위도 순서
    params = {
        'origin': f'{origin_lng},{origin_lat}',
        'destination': f'{destination_lng},{destination_lat}',
        'priority': priority,
        'alternatives': 'false',
        'road_details': 'true',
        'summary': 'false',
        'car_fuel': 'GASOLINE',
        'car_hipass': 'false',
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print('Kakao route search error:', error)
        return Response(
            {'message': '카카오 경로 검색 중 오류가 발생했습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(response.json(), status=response.status_code)