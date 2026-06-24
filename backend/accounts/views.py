from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import (
    SignupSerializer,
    UserSerializer,
    UserUpdateSerializer,
    FindUsernameSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    WithdrawSerializer,
)
from .models import UserProfile

def get_first_error_message(errors):
    if isinstance(errors, dict):
        if 'message' in errors:
            message = errors['message']

            if isinstance(message, list):
                return message[0]

            return message

        for value in errors.values():
            if isinstance(value, list) and len(value) > 0:
                return value[0]

            if isinstance(value, dict):
                return get_first_error_message(value)

            if isinstance(value, str):
                return value

    if isinstance(errors, list) and len(errors) > 0:
        return errors[0]

    return '입력값을 확인해주세요.'

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                'message': '회원가입이 완료되었습니다.',
                'user': UserSerializer(
                    user,
                    context={'request': request}
                ).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            'message': get_first_error_message(serializer.errors),
            'errors': serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'message': '아이디와 비밀번호를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response(
            {'message': '아이디 또는 비밀번호가 올바르지 않습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    token, created = Token.objects.get_or_create(user=user)

    UserProfile.objects.get_or_create(user=user)

    return Response({
        'message': '로그인되었습니다.',
        'token': token.key,
        'user': UserSerializer(
            user,
            context={'request': request}
        ).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response({'message': '로그아웃되었습니다.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    UserProfile.objects.get_or_create(user=request.user)

    serializer = UserSerializer(
        request.user,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_profile(request):
    UserProfile.objects.get_or_create(user=request.user)

    serializer = UserUpdateSerializer(
        request.user,
        data=request.data,
        partial=True,
        context={'request': request}
    )

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                'message': '회원정보가 수정되었습니다.',
                'user': UserSerializer(
                    user,
                    context={'request': request}
                ).data
            },
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def mask_username(username):
    if len(username) <= 2:
        return username[0] + '*'

    if len(username) <= 4:
        return username[0] + '*' * (len(username) - 1)

    return username[:4] + '*' * (len(username) - 6) + username[-2:]


@api_view(['POST'])
@permission_classes([AllowAny])
def find_username(request):
    serializer = FindUsernameSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {
                'message': get_first_error_message(serializer.errors),
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    email = serializer.validated_data['email']

    users = User.objects.filter(
        email__iexact=email,
        is_active=True
    ).order_by('id')

    usernames = [
        {
            'username': mask_username(user.username),
            'created_at': user.date_joined.strftime('%Y-%m-%d'),
        }
        for user in users
    ]

    return Response({
        'message': '아이디 찾기가 완료되었습니다.',
        'usernames': usernames,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        Token.objects.filter(user=user).delete()

        return Response({
            'message': '비밀번호가 재설정되었습니다. 새 비밀번호로 로그인해주세요.'
        })

    return Response(
        {
            'message': get_first_error_message(serializer.errors),
            'errors': serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        user = serializer.save()

        Token.objects.filter(user=user).delete()
        logout(request)

        return Response({
            'message': '비밀번호가 변경되었습니다. 다시 로그인해주세요.'
        })

    return Response(
        {
            'message': get_first_error_message(serializer.errors),
            'errors': serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    serializer = WithdrawSerializer(
        data=request.data,
        context={'request': request}
    )

    if not serializer.is_valid():
        return Response(
            {
                'message': get_first_error_message(serializer.errors),
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user
    user.is_active = False
    user.save()

    Token.objects.filter(user=user).delete()
    logout(request)

    return Response({
        'message': '회원탈퇴가 완료되었습니다.'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def profile_options(request):
    age_options = [
        {
            'value': age,
            'label': f'{age}세',
        }
        for age in range(19, 71)
    ]

    income_options = [
        {
            'value': value,
            'label': label,
        }
        for value, label in UserProfile.MONTHLY_INCOME_CHOICES
    ]

    saving_options = [
        {
            'value': value,
            'label': label,
        }
        for value, label in UserProfile.MONTHLY_SAVING_CHOICES
    ]

    lump_sum_options = [
        {
            'value': value,
            'label': label,
        }
        for value, label in UserProfile.LUMP_SUM_CHOICES
    ]

    bank_options = [
        {'value': '국민은행', 'label': '국민은행'},
        {'value': '신한은행', 'label': '신한은행'},
        {'value': '우리은행', 'label': '우리은행'},
        {'value': '하나은행', 'label': '하나은행'},
        {'value': '농협은행', 'label': '농협은행'},
        {'value': '기업은행', 'label': '기업은행'},
        {'value': '카카오뱅크', 'label': '카카오뱅크'},
        {'value': '케이뱅크', 'label': '케이뱅크'},
        {'value': '토스뱅크', 'label': '토스뱅크'},
        {'value': 'SC제일은행', 'label': 'SC제일은행'},
        {'value': '부산은행', 'label': '부산은행'},
        {'value': '대구은행', 'label': '대구은행'},
        {'value': '광주은행', 'label': '광주은행'},
        {'value': '전북은행', 'label': '전북은행'},
        {'value': '경남은행', 'label': '경남은행'},
        {'value': '제주은행', 'label': '제주은행'},
    ]

    region_options = [
        {'value': '서울특별시', 'label': '서울특별시'},
        {'value': '부산광역시', 'label': '부산광역시'},
        {'value': '대구광역시', 'label': '대구광역시'},
        {'value': '인천광역시', 'label': '인천광역시'},
        {'value': '광주광역시', 'label': '광주광역시'},
        {'value': '대전광역시', 'label': '대전광역시'},
        {'value': '울산광역시', 'label': '울산광역시'},
        {'value': '세종특별자치시', 'label': '세종특별자치시'},
        {'value': '경기도', 'label': '경기도'},
        {'value': '강원특별자치도', 'label': '강원특별자치도'},
        {'value': '충청북도', 'label': '충청북도'},
        {'value': '충청남도', 'label': '충청남도'},
        {'value': '전북특별자치도', 'label': '전북특별자치도'},
        {'value': '전라남도', 'label': '전라남도'},
        {'value': '경상북도', 'label': '경상북도'},
        {'value': '경상남도', 'label': '경상남도'},
        {'value': '제주특별자치도', 'label': '제주특별자치도'},
    ]

    return Response({
        'age': age_options,
        'monthly_income_range': income_options,
        'monthly_saving_amount': saving_options,
        'lump_sum_amount': lump_sum_options,
        'main_bank': bank_options,
        'address': region_options,
    })