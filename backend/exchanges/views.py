import requests
from datetime import datetime, timedelta

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


EXCHANGE_API_URL = 'https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON'
MAX_HISTORY_DAYS = 31


def parse_date(value):
    """
    YYYY-MM-DD 또는 YYYYMMDD 문자열을 datetime으로 변환
    """
    if not value:
        return datetime.today()

    value = str(value).strip()

    for date_format in ('%Y-%m-%d', '%Y%m%d'):
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    return None


def parse_rate(rate_text):
    """
    API 환율값이 '1,380.50'처럼 문자열로 오는 경우 숫자로 변환
    """
    if rate_text is None:
        return None

    try:
        return float(str(rate_text).replace(',', '').strip())
    except ValueError:
        return None


def normalize_currency_code(currency_code):
    """
    한국수출입은행 API의 JPY(100) 같은 표기를 JPY + 100단위로 정리
    """
    code = str(currency_code or '').strip()

    if '(100)' in code:
        base_code = code.replace('(100)', '').strip()
        return base_code, 100, f'100 {base_code}'

    return code, 1, f'1 {code}'


def get_exchange_rates_from_api(search_date=None, fallback_days=7):
    """
    특정 날짜 환율 조회.
    데이터가 없는 주말/공휴일이면 fallback_days 범위 안에서 이전 영업일 데이터를 찾음.
    """
    api_key = settings.EXCHANGE_API_KEY

    if not api_key:
        return None, None, 'EXCHANGE_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인해주세요.'

    base_date = search_date or datetime.today()

    for i in range(fallback_days + 1):
        current_date = base_date - timedelta(days=i)

        # 주말은 건너뛰기
        if current_date.weekday() >= 5:
            continue

        params = {
            'authkey': api_key,
            'searchdate': current_date.strftime('%Y%m%d'),
            'data': 'AP01',
        }

        try:
            response = requests.get(
                EXCHANGE_API_URL,
                params=params,
                timeout=8,
            )
        except requests.RequestException:
            continue

        if response.status_code != 200:
            continue

        try:
            data = response.json()
        except ValueError:
            continue

        if isinstance(data, list) and len(data) > 0:
            return data, current_date, None

    return None, None, '해당 날짜 주변의 환율 데이터를 찾을 수 없습니다. 주말 또는 공휴일일 수 있습니다.'


def build_rates(data):
    rates = []

    for item in data:
        raw_code = item.get('cur_unit')
        base_code, unit, display_unit = normalize_currency_code(raw_code)
        raw_rate = parse_rate(item.get('deal_bas_r'))

        if not base_code or raw_rate is None:
            continue

        rates.append({
            'currency_code': raw_code,
            'normalized_code': base_code,
            'currency_name': item.get('cur_nm'),
            'rate': item.get('deal_bas_r'),
            'raw_rate': raw_rate,
            'unit': unit,
            'rate_per_unit': raw_rate / unit,
            'display_unit': display_unit,
        })

    return rates


def find_rate_by_currency(data, currency):
    target_currency = str(currency or '').strip().upper()

    for item in data:
        raw_code = item.get('cur_unit')
        base_code, unit, display_unit = normalize_currency_code(raw_code)

        if base_code.upper() == target_currency:
            raw_rate = parse_rate(item.get('deal_bas_r'))

            if raw_rate is None:
                return None

            return {
                'currency_code': raw_code,
                'normalized_code': base_code,
                'currency_name': item.get('cur_nm'),
                'raw_rate': raw_rate,
                'unit': unit,
                'rate_per_unit': raw_rate / unit,
                'display_unit': display_unit,
            }

    return None


@api_view(['GET'])
def exchange_rate_list(request):
    selected_date = parse_date(request.GET.get('date'))

    if selected_date is None:
        return Response(
            {'message': 'date는 YYYY-MM-DD 형식으로 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    data, actual_date, error = get_exchange_rates_from_api(
        search_date=selected_date,
        fallback_days=7,
    )

    if error:
        return Response(
            {'message': error},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        'requested_date': selected_date.strftime('%Y-%m-%d'),
        'date': actual_date.strftime('%Y-%m-%d'),
        'rates': build_rates(data),
    })


@api_view(['GET'])
def exchange_rate_history(request):
    currency = request.GET.get('currency', 'USD').upper()
    start_date = parse_date(request.GET.get('start_date'))
    end_date = parse_date(request.GET.get('end_date'))

    if start_date is None or end_date is None:
        return Response(
            {'message': 'start_date와 end_date는 YYYY-MM-DD 형식으로 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if start_date > end_date:
        return Response(
            {'message': '시작일은 종료일보다 늦을 수 없습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    total_days = (end_date - start_date).days + 1

    if total_days > MAX_HISTORY_DAYS:
        return Response(
            {'message': f'기간별 그래프는 최대 {MAX_HISTORY_DAYS}일까지만 조회할 수 있습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    rows = []
    current_date = start_date

    while current_date <= end_date:
        # 주말은 한국수출입은행 데이터가 없는 경우가 많아서 건너뜀
        if current_date.weekday() < 5:
            data, actual_date, error = get_exchange_rates_from_api(
                search_date=current_date,
                fallback_days=0,
            )

            if data:
                target = find_rate_by_currency(data, currency)

                if target:
                    rows.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'currency_code': target['normalized_code'],
                        'currency_name': target['currency_name'],
                        'rate': round(target['rate_per_unit'], 4),
                        'display_unit': target['display_unit'],
                    })

        current_date += timedelta(days=1)

    if not rows:
        return Response(
            {
                'message': '해당 기간의 환율 데이터를 찾을 수 없습니다. 주말, 공휴일 또는 지원하지 않는 통화일 수 있습니다.',
                'currency': currency,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'rows': [],
            },
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        'currency': currency,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'count': len(rows),
        'rows': rows,
    })


@api_view(['POST'])
def exchange_calculate(request):
    amount = request.data.get('amount')
    currency = request.data.get('currency')
    selected_date = parse_date(request.data.get('date'))

    if amount is None or not currency:
        return Response(
            {'message': 'amount와 currency를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if selected_date is None:
        return Response(
            {'message': 'date는 YYYY-MM-DD 형식으로 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        amount = float(amount)
    except ValueError:
        return Response(
            {'message': 'amount는 숫자여야 합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    data, actual_date, error = get_exchange_rates_from_api(
        search_date=selected_date,
        fallback_days=7,
    )

    if error:
        return Response(
            {'message': error},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    target = find_rate_by_currency(data, currency)

    if target is None:
        return Response(
            {'message': '해당 통화 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    converted_amount = amount / target['rate_per_unit']

    return Response({
        'date': actual_date.strftime('%Y-%m-%d'),
        'amount_krw': amount,
        'currency': target['normalized_code'],
        'currency_name': target['currency_name'],
        'rate': target['rate_per_unit'],
        'converted_amount': round(converted_amount, 2),
    })