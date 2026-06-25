import requests

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Bank, FinancialProduct, ProductOption
from .serializers import (
    FinancialProductListSerializer,
    FinancialProductDetailSerializer,
)


def save_products_from_fss(product_type):
    """
    금감원 예금/적금 API 데이터를 DB에 저장하는 공통 함수

    product_type:
    - deposit: 정기예금
    - saving: 적금
    """
    api_key = settings.FSS_API_KEY

    if not api_key:
        return {
            'success': False,
            'message': 'FSS_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인해주세요.',
            'status_code': 500,
        }

    if product_type == 'deposit':
        url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
        success_message = '정기예금 상품 저장 완료'
        fail_message = '금감원 예금 API 요청에 실패했습니다.'
    elif product_type == 'saving':
        url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
        success_message = '적금 상품 저장 완료'
        fail_message = '금감원 적금 API 요청에 실패했습니다.'
    else:
        return {
            'success': False,
            'message': '올바르지 않은 상품 유형입니다.',
            'status_code': 400,
        }

    saved_banks = 0
    saved_products = 0
    saved_options = 0
    total_base_count = 0
    total_option_count = 0

    page_no = 1
    max_page_no = 1

    while page_no <= max_page_no:
        params = {
            'auth': api_key,
            'topFinGrpNo': '020000',
            'pageNo': page_no,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
        except requests.RequestException as error:
            return {
                'success': False,
                'message': fail_message,
                'error': str(error),
                'status_code': 500,
            }

        if response.status_code != 200:
            return {
                'success': False,
                'message': fail_message,
                'fss_status_code': response.status_code,
                'status_code': 500,
            }

        data = response.json()
        result = data.get('result', {})

        max_page_no = int(result.get('max_page_no') or 1)

        base_list = result.get('baseList', [])
        option_list = result.get('optionList', [])

        total_base_count += len(base_list)
        total_option_count += len(option_list)

        # 1. 상품 기본 정보 저장
        for item in base_list:
            bank, bank_created = Bank.objects.get_or_create(
                code=item.get('fin_co_no'),
                defaults={
                    'name': item.get('kor_co_nm', '')
                }
            )

            if bank_created:
                saved_banks += 1

            product, product_created = FinancialProduct.objects.update_or_create(
                bank=bank,
                fin_prdt_cd=item.get('fin_prdt_cd'),
                product_type=product_type,
                defaults={
                    'name': item.get('fin_prdt_nm') or '',
                    'join_way': item.get('join_way') or '',
                    'mtrt_int': item.get('mtrt_int') or '',
                    'spcl_cnd': item.get('spcl_cnd') or '',
                    'join_deny': str(item.get('join_deny') or ''),
                    'join_member': item.get('join_member') or '',
                    'etc_note': item.get('etc_note') or '',
                    'max_limit': item.get('max_limit'),
                    'dcls_month': item.get('dcls_month') or '',
                    'dcls_strt_day': item.get('dcls_strt_day') or '',
                    'dcls_end_day': item.get('dcls_end_day') or '',
                    'fin_co_subm_day': item.get('fin_co_subm_day') or '',
                }
            )

            if product_created:
                saved_products += 1

        # 2. 금리 옵션 저장
        for option in option_list:
            bank_code = option.get('fin_co_no')
            product_code = option.get('fin_prdt_cd')
            save_trm = option.get('save_trm')

            if not save_trm:
                continue

            try:
                product = FinancialProduct.objects.get(
                    bank__code=bank_code,
                    fin_prdt_cd=product_code,
                    product_type=product_type,
                )
            except FinancialProduct.DoesNotExist:
                continue

            product_option, option_created = ProductOption.objects.update_or_create(
                product=product,
                intr_rate_type=option.get('intr_rate_type', ''),
                rsrv_type=option.get('rsrv_type', ''),
                save_trm=int(save_trm),
                defaults={
                    'intr_rate_type_nm': option.get('intr_rate_type_nm', ''),
                    'rsrv_type_nm': option.get('rsrv_type_nm', ''),
                    'intr_rate': option.get('intr_rate') or None,
                    'intr_rate2': option.get('intr_rate2') or None,
                }
            )

            if option_created:
                saved_options += 1

        page_no += 1

    return {
        'success': True,
        'message': success_message,
        'saved_banks': saved_banks,
        'saved_products': saved_products,
        'saved_options': saved_options,
        'total_base_count': total_base_count,
        'total_option_count': total_option_count,
        'status_code': 200,
    }


def ensure_products_exist(product_type):
    """
    해당 상품 유형의 DB 데이터가 비어 있으면 금감원 API에서 자동 저장
    이미 데이터가 있으면 아무것도 하지 않음
    """
    exists = FinancialProduct.objects.filter(product_type=product_type).exists()

    if exists:
        return {
            'success': True,
            'message': '이미 저장된 상품 데이터가 있습니다.',
            'status_code': 200,
        }

    return save_products_from_fss(product_type)


@api_view(['GET'])
@permission_classes([AllowAny])
def save_deposit_products(request):
    result = save_products_from_fss('deposit')

    if not result.get('success'):
        return Response(result, status=result.get('status_code', 500))

    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def deposit_product_list(request):
    init_result = ensure_products_exist('deposit')

    if not init_result.get('success'):
        return Response(init_result, status=init_result.get('status_code', 500))

    products = FinancialProduct.objects.filter(
        product_type='deposit'
    ).prefetch_related('options').select_related('bank')

    serializer = FinancialProductListSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def deposit_product_detail(request, product_id):
    init_result = ensure_products_exist('deposit')

    if not init_result.get('success'):
        return Response(init_result, status=init_result.get('status_code', 500))

    try:
        product = FinancialProduct.objects.select_related('bank').prefetch_related('options').get(
            id=product_id,
            product_type='deposit'
        )
    except FinancialProduct.DoesNotExist:
        return Response(
            {'message': '해당 정기예금 상품을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = FinancialProductDetailSerializer(product)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def save_saving_products(request):
    result = save_products_from_fss('saving')

    if not result.get('success'):
        return Response(result, status=result.get('status_code', 500))

    return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny])
def saving_product_list(request):
    init_result = ensure_products_exist('saving')

    if not init_result.get('success'):
        return Response(init_result, status=init_result.get('status_code', 500))

    products = FinancialProduct.objects.filter(
        product_type='saving'
    ).prefetch_related('options').select_related('bank')

    serializer = FinancialProductListSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def saving_product_detail(request, product_id):
    init_result = ensure_products_exist('saving')

    if not init_result.get('success'):
        return Response(init_result, status=init_result.get('status_code', 500))

    try:
        product = FinancialProduct.objects.select_related('bank').prefetch_related('options').get(
            id=product_id,
            product_type='saving'
        )
    except FinancialProduct.DoesNotExist:
        return Response(
            {'message': '해당 적금 상품을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = FinancialProductDetailSerializer(product)

    return Response(serializer.data)