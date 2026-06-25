import requests
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import ExchangeRate


EXCHANGE_API_URL = 'https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON'
MAX_HISTORY_DAYS = 31
MAX_SAVE_DAYS = 90


def parse_date(value):
    """YYYY-MM-DD 또는 YYYYMMDD 문자열을 datetime으로 변환한다."""
    if not value:
        return datetime.today()

    value = str(value).strip()

    for date_format in ('%Y-%m-%d', '%Y%m%d'):
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    return None


def parse_bool(value):
    return str(value or '').strip().lower() in ('1', 'true', 'yes', 'y')


def parse_rate(rate_text):
    """API 환율값이 '1,380.50'처럼 문자열로 오는 경우 숫자로 변환한다."""
    if rate_text is None:
        return None

    try:
        return float(str(rate_text).replace(',', '').strip())
    except ValueError:
        return None


def normalize_currency_code(currency_code):
    """한국수출입은행 API의 JPY(100) 같은 표기를 JPY + 100단위로 정리한다."""
    code = str(currency_code or '').strip()

    if '(100)' in code:
        base_code = code.replace('(100)', '').strip()
        return base_code, 100, f'100 {base_code}'

    return code, 1, f'1 {code}'


def get_exchange_rates_from_api(search_date=None, fallback_days=7):
    """한국수출입은행 API에서 특정 날짜 환율을 조회한다.

    주말/공휴일처럼 데이터가 없으면 fallback_days 범위 안에서 이전 영업일 데이터를 찾는다.
    """
    api_key = getattr(settings, 'EXCHANGE_API_KEY', '')

    if not api_key:
        return None, None, 'EXCHANGE_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인해주세요.'

    base_date = search_date or datetime.today()
    last_error = None

    for i in range(fallback_days + 1):
        current_date = base_date - timedelta(days=i)

        # 한국수출입은행 환율은 주말 데이터가 없는 경우가 많아서 주말은 건너뛴다.
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
                verify=False,
            )
        except requests.RequestException as exc:
            last_error = str(exc)
            continue

        if response.status_code != 200:
            last_error = f'API 응답 상태 코드 {response.status_code}'
            continue

        try:
            data = response.json()
        except ValueError:
            last_error = 'API 응답을 JSON으로 변환하지 못했습니다.'
            continue

        if isinstance(data, list) and len(data) > 0:
            usable_items = [item for item in data if item.get('cur_unit') and item.get('deal_bas_r')]

            if usable_items:
                return usable_items, current_date, None

        last_error = 'API 응답에 환율 데이터가 없습니다.'

    return None, None, last_error or '해당 날짜 주변의 환율 데이터를 찾을 수 없습니다. 주말 또는 공휴일일 수 있습니다.'


def save_api_rates_to_db(data, actual_date):
    """API 조회 성공 데이터를 ExchangeRate DB에 저장한다."""
    if not data or not actual_date:
        return {
            'saved_count': 0,
            'updated_count': 0,
            'skipped_count': 0,
        }

    saved_count = 0
    updated_count = 0
    skipped_count = 0

    for item in data:
        raw_code = item.get('cur_unit')
        base_code, unit, display_unit = normalize_currency_code(raw_code)
        raw_rate = parse_rate(item.get('deal_bas_r'))

        if not base_code or raw_rate is None:
            skipped_count += 1
            continue

        try:
            raw_rate_decimal = Decimal(str(raw_rate))
            rate_per_unit_decimal = Decimal(str(raw_rate / unit))
        except (InvalidOperation, ZeroDivisionError):
            skipped_count += 1
            continue

        _, created = ExchangeRate.objects.update_or_create(
            date=actual_date.date(),
            normalized_code=base_code,
            defaults={
                'currency_code': raw_code,
                'currency_name': item.get('cur_nm') or base_code,
                'raw_rate': raw_rate_decimal,
                'rate_per_unit': rate_per_unit_decimal,
                'unit': unit,
                'display_unit': display_unit,
                'source': 'koreaexim_api',
            },
        )

        if created:
            saved_count += 1
        else:
            updated_count += 1

    return {
        'saved_count': saved_count,
        'updated_count': updated_count,
        'skipped_count': skipped_count,
    }


def get_exact_db_rates(date_value):
    """특정 날짜의 DB 환율 데이터를 조회한다."""
    rows = list(
        ExchangeRate.objects
        .filter(date=date_value.date())
        .order_by('normalized_code')
    )
    return rows


def get_nearest_db_rates(search_date=None):
    """선택 날짜 이전의 가장 가까운 DB 환율 데이터를 조회한다.

    API 장애 시 fixture fallback 용도로 사용한다.
    """
    base_date = (search_date or datetime.today()).date()

    actual_date = (
        ExchangeRate.objects
        .filter(date__lte=base_date)
        .order_by('-date')
        .values_list('date', flat=True)
        .first()
    )

    if actual_date is None:
        actual_date = (
            ExchangeRate.objects
            .order_by('date')
            .values_list('date', flat=True)
            .first()
        )

    if actual_date is None:
        return [], None

    rows = list(
        ExchangeRate.objects
        .filter(date=actual_date)
        .order_by('normalized_code')
    )

    return rows, datetime.combine(actual_date, datetime.min.time())


def ensure_exchange_rates_exist(search_date=None, fallback_days=7, force_api=False):
    """예적금 상품 ensure_products_exist와 같은 역할.

    1. DB에 해당 날짜 데이터가 있으면 API를 호출하지 않는다.
    2. DB에 없으면 한국수출입은행 API에서 가져와 DB에 저장한다.
    3. API가 실패하면 fixture로 넣어둔 DB의 가장 가까운 날짜 데이터를 사용한다.
    """
    selected_date = search_date or datetime.today()

    if not force_api:
        exact_rows = get_exact_db_rates(selected_date)

        if exact_rows:
            return {
                'success': True,
                'message': '이미 저장된 환율 데이터가 있습니다.',
                'requested_date': selected_date,
                'actual_date': selected_date,
                'rows': exact_rows,
                'source': 'db',
                'source_label': 'DB 저장 환율',
                'api_called': False,
                'fallback_used': False,
                'status_code': 200,
            }

    data, actual_date, api_error = get_exchange_rates_from_api(
        search_date=selected_date,
        fallback_days=fallback_days,
    )

    if data:
        save_result = save_api_rates_to_db(data, actual_date)
        rows = get_exact_db_rates(actual_date)

        return {
            'success': True,
            'message': '한국수출입은행 API 환율 데이터 저장 완료',
            'requested_date': selected_date,
            'actual_date': actual_date,
            'rows': rows,
            'source': 'koreaexim_api',
            'source_label': '한국수출입은행 API 저장 데이터',
            'api_called': True,
            'fallback_used': False,
            'save_result': save_result,
            'status_code': 200,
        }

    fallback_rows, fallback_date = get_nearest_db_rates(selected_date)

    if fallback_rows:
        return {
            'success': True,
            'message': 'API 호출 실패로 DB 저장 환율 데이터를 사용합니다.',
            'requested_date': selected_date,
            'actual_date': fallback_date,
            'rows': fallback_rows,
            'source': 'fixture',
            'source_label': 'DB 저장 환율',
            'api_called': True,
            'fallback_used': True,
            'fallback_reason': api_error,
            'status_code': 200,
        }

    return {
        'success': False,
        'message': '환율 데이터를 찾을 수 없습니다. API 키를 확인하거나 python manage.py loaddata exchange_rates.json 을 실행해주세요.',
        'api_error': api_error,
        'status_code': 500,
    }


def build_rates_from_db(rows):
    """ExchangeRate 모델 데이터를 프론트에서 사용하는 형식으로 변환한다."""
    rates = []

    for item in rows:
        rates.append({
            'currency_code': item.currency_code,
            'normalized_code': item.normalized_code,
            'currency_name': item.currency_name,
            'rate': f'{float(item.raw_rate):,.4f}',
            'raw_rate': float(item.raw_rate),
            'unit': item.unit,
            'rate_per_unit': float(item.rate_per_unit),
            'display_unit': item.display_unit,
            'source': item.source,
        })

    return rates


def find_rate_by_currency_from_db(rows, currency):
    """DB 조회 결과에서 특정 통화 정보를 찾는다."""
    target_currency = str(currency or '').strip().upper()

    for item in rows:
        if item.normalized_code.upper() == target_currency:
            return {
                'currency_code': item.currency_code,
                'normalized_code': item.normalized_code,
                'currency_name': item.currency_name,
                'raw_rate': float(item.raw_rate),
                'unit': item.unit,
                'rate_per_unit': float(item.rate_per_unit),
                'display_unit': item.display_unit,
                'source': item.source,
            }

    return None


def get_source_mode(request):
    if request.method == 'POST':
        source = request.data.get('source') or request.GET.get('source')
    else:
        source = request.GET.get('source')

    return str(source or 'auto').strip().lower()


def is_force_api(request):
    return get_source_mode(request) in ('api', 'live')


def is_fixture_only(request):
    return get_source_mode(request) in ('fixture', 'db', 'local')


@api_view(['GET'])
@permission_classes([AllowAny])
def save_exchange_rates(request):
    """한국수출입은행 API 데이터를 DB에 저장한다.

    products/views.py의 deposits/save, savings/save와 같은 성격의 엔드포인트다.

    사용 예시:
    - /api/exchanges/rates/save/?date=2026-06-26
    - /api/exchanges/rates/save/?start_date=2026-06-01&end_date=2026-06-26
    - /api/exchanges/rates/save/?start_date=2026-06-01&end_date=2026-06-26&reset=1
    """
    selected_date = parse_date(request.GET.get('date'))
    start_date = parse_date(request.GET.get('start_date'))
    end_date = parse_date(request.GET.get('end_date'))
    reset = parse_bool(request.GET.get('reset'))

    if selected_date is None or start_date is None or end_date is None:
        return Response(
            {'message': 'date, start_date, end_date는 YYYY-MM-DD 형식으로 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # start_date/end_date가 명시되지 않으면 date 또는 오늘 하루만 저장한다.
    has_range = request.GET.get('start_date') or request.GET.get('end_date')

    if not has_range:
        start_date = selected_date
        end_date = selected_date

    if start_date > end_date:
        return Response(
            {'message': '시작일은 종료일보다 늦을 수 없습니다.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    total_days = (end_date - start_date).days + 1

    if total_days > MAX_SAVE_DAYS:
        return Response(
            {'message': f'한 번에 저장할 수 있는 환율 기간은 최대 {MAX_SAVE_DAYS}일입니다.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if reset:
        ExchangeRate.objects.filter(
            date__gte=start_date.date(),
            date__lte=end_date.date(),
        ).delete()

    current_date = start_date
    total_saved = 0
    total_updated = 0
    total_skipped = 0
    success_dates = []
    failed_dates = []

    while current_date <= end_date:
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue

        data, actual_date, error = get_exchange_rates_from_api(
            search_date=current_date,
            fallback_days=0,
        )

        if data:
            save_result = save_api_rates_to_db(data, actual_date)
            total_saved += save_result['saved_count']
            total_updated += save_result['updated_count']
            total_skipped += save_result['skipped_count']
            success_dates.append(actual_date.strftime('%Y-%m-%d'))
        else:
            failed_dates.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'error': error,
            })

        current_date += timedelta(days=1)

    return Response({
        'success': True,
        'message': '한국수출입은행 API 환율 데이터 저장 작업이 완료되었습니다.',
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'saved_count': total_saved,
        'updated_count': total_updated,
        'skipped_count': total_skipped,
        'success_dates': sorted(set(success_dates)),
        'failed_dates': failed_dates,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate_list(request):
    selected_date = parse_date(request.GET.get('date'))

    if selected_date is None:
        return Response(
            {'message': 'date는 YYYY-MM-DD 형식으로 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if is_fixture_only(request):
        rows, actual_date = get_nearest_db_rates(selected_date)
        if not rows:
            return Response(
                {'message': 'DB에 저장된 환율 데이터가 없습니다. python manage.py loaddata exchange_rates.json 을 실행해주세요.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({
            'requested_date': selected_date.strftime('%Y-%m-%d'),
            'date': actual_date.strftime('%Y-%m-%d'),
            'source': 'fixture',
            'source_label': 'DB 저장 환율',
            'api_called': False,
            'fallback_used': False,
            'rates': build_rates_from_db(rows),
        })

    result = ensure_exchange_rates_exist(
        search_date=selected_date,
        fallback_days=7,
        force_api=is_force_api(request),
    )

    if not result.get('success'):
        return Response(result, status=result.get('status_code', 500))

    return Response({
        'requested_date': selected_date.strftime('%Y-%m-%d'),
        'date': result['actual_date'].strftime('%Y-%m-%d'),
        'source': result['source'],
        'source_label': result['source_label'],
        'api_called': result.get('api_called', False),
        'fallback_used': result.get('fallback_used', False),
        'fallback_reason': result.get('fallback_reason'),
        'rates': build_rates_from_db(result['rows']),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate_history(request):
    currency = request.GET.get('currency', 'USD').upper()
    start_date = parse_date(request.GET.get('start_date'))
    end_date = parse_date(request.GET.get('end_date'))

    if start_date is None or end_date is None:
        return Response(
            {'message': 'start_date와 end_date는 YYYY-MM-DD 형식으로 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if start_date > end_date:
        return Response(
            {'message': '시작일은 종료일보다 늦을 수 없습니다.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    total_days = (end_date - start_date).days + 1

    if total_days > MAX_HISTORY_DAYS:
        return Response(
            {'message': f'기간별 그래프는 최대 {MAX_HISTORY_DAYS}일까지만 조회할 수 있습니다.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    api_called = False
    api_errors = []

    # fixture 강제 모드가 아니면, DB에 없는 날짜만 API에서 가져와 저장한다.
    if not is_fixture_only(request):
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() < 5:
                exists = ExchangeRate.objects.filter(
                    date=current_date.date(),
                    normalized_code=currency,
                ).exists()

                if not exists or is_force_api(request):
                    api_called = True
                    data, actual_date, error = get_exchange_rates_from_api(
                        search_date=current_date,
                        fallback_days=0,
                    )

                    if data:
                        save_api_rates_to_db(data, actual_date)
                    elif error:
                        api_errors.append({
                            'date': current_date.strftime('%Y-%m-%d'),
                            'error': error,
                        })

            current_date += timedelta(days=1)

    db_rows = list(
        ExchangeRate.objects
        .filter(
            normalized_code=currency,
            date__gte=start_date.date(),
            date__lte=end_date.date(),
        )
        .order_by('date')
    )

    if not db_rows:
        return Response(
            {
                'message': '해당 기간의 환율 데이터를 찾을 수 없습니다. API 키를 확인하거나 python manage.py loaddata exchange_rates.json 을 실행해주세요.',
                'currency': currency,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'api_called': api_called,
                'api_errors': api_errors,
                'rows': [],
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    rows = [
        {
            'date': item.date.strftime('%Y-%m-%d'),
            'currency_code': item.normalized_code,
            'currency_name': item.currency_name,
            'rate': round(float(item.rate_per_unit), 4),
            'display_unit': item.display_unit,
            'source': item.source,
        }
        for item in db_rows
    ]

    return Response({
        'currency': currency,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'source': 'db',
        'source_label': 'DB 저장 환율',
        'api_called': api_called,
        'fallback_used': bool(api_errors),
        'api_errors': api_errors,
        'count': len(rows),
        'rows': rows,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def exchange_calculate(request):
    amount = request.data.get('amount')
    currency = request.data.get('currency')
    selected_date = parse_date(request.data.get('date'))

    if amount is None or not currency:
        return Response(
            {'message': 'amount와 currency를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if selected_date is None:
        return Response(
            {'message': 'date는 YYYY-MM-DD 형식으로 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        amount = float(amount)
    except ValueError:
        return Response(
            {'message': 'amount는 숫자여야 합니다.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if is_fixture_only(request):
        rows, actual_date = get_nearest_db_rates(selected_date)
        if not rows:
            return Response(
                {'message': 'DB에 저장된 환율 데이터가 없습니다. python manage.py loaddata exchange_rates.json 을 실행해주세요.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        result = ensure_exchange_rates_exist(
            search_date=selected_date,
            fallback_days=7,
            force_api=is_force_api(request),
        )

        if not result.get('success'):
            return Response(result, status=result.get('status_code', 500))

        rows = result['rows']
        actual_date = result['actual_date']

    target = find_rate_by_currency_from_db(rows, currency)

    if target is None:
        return Response(
            {'message': '해당 통화 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    converted_amount = amount / target['rate_per_unit']

    return Response({
        'date': actual_date.strftime('%Y-%m-%d'),
        'amount_krw': amount,
        'currency': target['normalized_code'],
        'currency_name': target['currency_name'],
        'rate': target['rate_per_unit'],
        'converted_amount': round(converted_amount, 2),
        'source': target['source'],
        'source_label': 'DB 저장 환율',
    })
