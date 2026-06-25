import re

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from products.models import Bank, FinancialProduct
from .models import BankTestResult
from .serializers import BankTestResultSerializer


def find_bank_by_keywords(keywords):
    for keyword in keywords:
        bank = Bank.objects.filter(name__icontains=keyword).first()
        if bank:
            return bank
    return Bank.objects.first()


def recommend_bank(data):
    access = data.get('access_preference')
    benefit = data.get('benefit_preference')
    stability = data.get('stability_preference')
    purpose = data.get('usage_purpose')

    # 1. 인터넷은행 선호
    if stability == 'internet_bank' or access == 'mobile':
        bank = find_bank_by_keywords(['카카오', '케이', '토스'])
        reason = (
            '모바일 접근성을 중요하게 생각하는 성향으로 보입니다. '
            '비대면 가입과 앱 사용 편의성을 고려해 인터넷은행 계열 상품이 잘 맞을 수 있습니다.'
        )
        return bank, reason

    # 2. 높은 금리 선호
    if benefit == 'high_interest' or purpose == 'interest':
        product = FinancialProduct.objects.filter(
            product_type='deposit',
            options__intr_rate2__isnull=False
        ).select_related('bank').order_by('-options__intr_rate2').first()

        if product:
            reason = (
                f'높은 금리를 중요하게 생각하는 성향으로 보입니다. '
                f'현재 저장된 정기예금 상품 중 금리 조건이 좋은 상품을 기준으로 '
                f'{product.bank.name}을 추천합니다.'
            )
            return product.bank, reason

    # 3. 안정성/시중은행 선호
    if stability == 'major_bank' or benefit == 'stability':
        bank = find_bank_by_keywords(['국민', '신한', '우리', '하나', '농협'])
        reason = (
            '안정성과 익숙한 금융거래를 중요하게 생각하는 성향으로 보입니다. '
            '시중은행 중심의 정기예금 상품이 잘 맞을 수 있습니다.'
        )
        return bank, reason

    # 4. 조건 단순 선호
    if benefit == 'simple_condition':
        product = FinancialProduct.objects.filter(
            product_type='deposit',
            spcl_cnd__icontains='해당사항 없음'
        ).select_related('bank').first()

        if product:
            reason = (
                '복잡한 우대조건보다 단순한 상품을 선호하는 성향으로 보입니다. '
                '우대조건이 비교적 단순한 정기예금 상품을 기준으로 추천했습니다.'
            )
            return product.bank, reason

    # 기본값
    bank = Bank.objects.first()
    reason = (
        '입력한 성향을 종합했을 때, 현재 저장된 정기예금 상품을 보유한 은행 중 '
        '기본 추천 은행을 제안합니다.'
    )
    return bank, reason


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def main_bank_recommendation(request):
    serializer = BankTestResultSerializer(data=request.data)

    if serializer.is_valid():
        bank, reason = recommend_bank(serializer.validated_data)

        result = BankTestResult.objects.create(
            user=request.user,
            recommended_bank=bank,
            access_preference=serializer.validated_data['access_preference'],
            benefit_preference=serializer.validated_data['benefit_preference'],
            stability_preference=serializer.validated_data['stability_preference'],
            usage_purpose=serializer.validated_data['usage_purpose'],
            reason=reason
        )

        return Response(
            BankTestResultSerializer(result).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_recommendation_history(request):
    results = BankTestResult.objects.filter(
        user=request.user
    ).select_related('recommended_bank').order_by('-created_at')

    serializer = BankTestResultSerializer(results, many=True)
    return Response(serializer.data)


AGE_NO_RESTRICTION_KEYWORDS = [
    '제한없음',
    '제한 없음',
    '누구나',
    '개인 및 개인사업자',
    '실명의 개인 및 개인사업자',
]


def normalize_age_text(text):
    if not text:
        return ''

    return re.sub(r'\s+', '', str(text))


def parse_age_rule(join_member):
    """
    금감원 상품의 가입대상(join_member) 문장에서 명시적인 나이 조건을 추출한다.
    반환값: (min_age, max_age, reason)
    - min_age/max_age가 None이면 해당 방향 제한 없음
    - 명시적인 나이 조건이 없으면 (None, None, '') 반환
    """
    original_text = str(join_member or '')
    compact_text = normalize_age_text(original_text)

    if not compact_text:
        return None, None, ''

    if any(normalize_age_text(keyword) in compact_text for keyword in AGE_NO_RESTRICTION_KEYWORDS):
        return None, None, ''

    min_age = None
    max_age = None
    rules = []

    # 예: 만 19세 이상 만 34세 이하, 만19세이상~만34세이하
    range_patterns = [
        r'만?(\d{1,2})세이상.*?만?(\d{1,2})세이하',
        r'만?(\d{1,2})세부터.*?만?(\d{1,2})세까지',
        r'만?(\d{1,2})세~만?(\d{1,2})세',
        r'만?(\d{1,2})세이상~?만?(\d{1,2})세이하',
    ]

    for pattern in range_patterns:
        match = re.search(pattern, compact_text)
        if match:
            lower = int(match.group(1))
            upper = int(match.group(2))
            min_age = lower if min_age is None else max(min_age, lower)
            max_age = upper if max_age is None else min(max_age, upper)
            rules.append(f'만 {lower}세 이상 만 {upper}세 이하')
            break

    # 예: 만 17세 미만, 17세미만
    for match in re.finditer(r'만?(\d{1,2})세미만', compact_text):
        age_limit = int(match.group(1)) - 1
        max_age = age_limit if max_age is None else min(max_age, age_limit)
        rules.append(f'만 {match.group(1)}세 미만')

    # 예: 만 19세 이하
    for match in re.finditer(r'만?(\d{1,2})세이하', compact_text):
        age_limit = int(match.group(1))
        max_age = age_limit if max_age is None else min(max_age, age_limit)
        rules.append(f'만 {age_limit}세 이하')

    # 예: 만 19세 초과
    for match in re.finditer(r'만?(\d{1,2})세초과', compact_text):
        age_limit = int(match.group(1)) + 1
        min_age = age_limit if min_age is None else max(min_age, age_limit)
        rules.append(f'만 {match.group(1)}세 초과')

    # 예: 만 19세 이상
    for match in re.finditer(r'만?(\d{1,2})세이상', compact_text):
        age_limit = int(match.group(1))
        min_age = age_limit if min_age is None else max(min_age, age_limit)
        rules.append(f'만 {age_limit}세 이상')

    return min_age, max_age, ', '.join(dict.fromkeys(rules))


def check_product_age_eligibility(product, user_age):
    """
    사용자 나이와 상품 가입대상(join_member)을 비교한다.
    나이를 알 수 없거나 가입대상에 명시적 나이 조건이 없으면 추천 후보에서 제외하지 않는다.
    """
    join_member = product.join_member or ''
    min_age, max_age, rule_description = parse_age_rule(join_member)

    if user_age in [None, '']:
        return {
            'eligible': True,
            'checked': False,
            'label': '가입대상 확인 필요',
            'reason': '사용자 나이 정보가 없어 가입대상 나이 조건을 필터링하지 않았습니다.',
            'min_age': min_age,
            'max_age': max_age,
            'rule_description': rule_description,
        }

    try:
        age = int(user_age)
    except (TypeError, ValueError):
        return {
            'eligible': True,
            'checked': False,
            'label': '가입대상 확인 필요',
            'reason': '사용자 나이 정보가 올바르지 않아 가입대상 나이 조건을 필터링하지 않았습니다.',
            'min_age': min_age,
            'max_age': max_age,
            'rule_description': rule_description,
        }

    if min_age is None and max_age is None:
        return {
            'eligible': True,
            'checked': True,
            'label': '가입 가능',
            'reason': '가입대상에 명시적인 나이 제한이 없어 추천 후보에 포함했습니다.',
            'min_age': None,
            'max_age': None,
            'rule_description': '',
        }

    if min_age is not None and age < min_age:
        return {
            'eligible': False,
            'checked': True,
            'label': '가입대상 제외',
            'reason': f'사용자 나이 {age}세가 가입대상 조건({rule_description})에 맞지 않습니다.',
            'min_age': min_age,
            'max_age': max_age,
            'rule_description': rule_description,
        }

    if max_age is not None and age > max_age:
        return {
            'eligible': False,
            'checked': True,
            'label': '가입대상 제외',
            'reason': f'사용자 나이 {age}세가 가입대상 조건({rule_description})에 맞지 않습니다.',
            'min_age': min_age,
            'max_age': max_age,
            'rule_description': rule_description,
        }

    return {
        'eligible': True,
        'checked': True,
        'label': '가입 가능',
        'reason': f'사용자 나이 {age}세가 가입대상 조건({rule_description})에 부합합니다.' if rule_description else '가입대상 조건에 부합합니다.',
        'min_age': min_age,
        'max_age': max_age,
        'rule_description': rule_description,
    }


GENDER_KEYWORD_RULES = {
    'female': [
        '여성전용', '여성 전용', '여성만', '여자만', '여성 고객', '여성고객',
        '여성', '여자', '여학생', '여대생', '미즈', '우먼', '레이디',
        'woman', 'women', 'lady', 'ladies',
    ],
    'male': [
        '남성전용', '남성 전용', '남성만', '남자만', '남성 고객', '남성고객',
        '남성', '남자', '남학생', '남자 대학생',
        'man', 'men',
    ],
}

GENDER_NEUTRAL_KEYWORDS = [
    '남녀', '성별무관', '성별 무관', '제한없음', '제한 없음', '누구나',
]


def normalize_gender_value(value):
    if value in [None, '']:
        return 'unknown'

    text = str(value).strip().lower()

    if text in ['male', 'm', 'man', '남성', '남자']:
        return 'male'

    if text in ['female', 'f', 'woman', '여성', '여자']:
        return 'female'

    return 'unknown'


def parse_gender_rule(product):
    """
    상품명/가입대상/우대조건 문장에서 성별 전용 상품 여부를 추정한다.
    금감원 데이터가 구조화된 성별 필드를 제공하지 않기 때문에 텍스트 기반으로 1차 필터링한다.
    """
    source_text = ' '.join([
        str(getattr(product, 'name', '') or ''),
        str(getattr(product, 'join_member', '') or ''),
        str(getattr(product, 'spcl_cnd', '') or ''),
        str(getattr(product, 'etc_note', '') or ''),
    ])
    compact_text = normalize_age_text(source_text).lower()

    if not compact_text:
        return None, ''

    if any(normalize_age_text(keyword).lower() in compact_text for keyword in GENDER_NEUTRAL_KEYWORDS):
        return None, ''

    for gender, keywords in GENDER_KEYWORD_RULES.items():
        for keyword in keywords:
            normalized_keyword = normalize_age_text(keyword).lower()
            if normalized_keyword and normalized_keyword in compact_text:
                label = '여성 전용' if gender == 'female' else '남성 전용'
                return gender, label

    return None, ''


def check_product_gender_eligibility(product, user_gender):
    required_gender, rule_description = parse_gender_rule(product)
    normalized_user_gender = normalize_gender_value(user_gender)

    if required_gender is None:
        return {
            'eligible': True,
            'checked': True,
            'label': '성별 제한 없음',
            'reason': '성별 전용 상품으로 판단되지 않아 추천 후보에 포함했습니다.',
            'required_gender': None,
            'rule_description': '',
        }

    if normalized_user_gender == 'unknown':
        return {
            'eligible': True,
            'checked': False,
            'label': '성별 확인 필요',
            'reason': f'{rule_description} 상품으로 보이나 사용자 성별 정보가 없어 제외하지 않았습니다.',
            'required_gender': required_gender,
            'rule_description': rule_description,
        }

    if normalized_user_gender != required_gender:
        user_gender_label = '여성' if normalized_user_gender == 'female' else '남성'
        return {
            'eligible': False,
            'checked': True,
            'label': '가입대상 제외',
            'reason': f'사용자 성별({user_gender_label})이 상품 가입대상({rule_description})과 맞지 않습니다.',
            'required_gender': required_gender,
            'rule_description': rule_description,
        }

    return {
        'eligible': True,
        'checked': True,
        'label': '가입 가능',
        'reason': f'사용자 성별 정보가 상품 가입대상({rule_description})에 부합합니다.',
        'required_gender': required_gender,
        'rule_description': rule_description,
    }

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_recommendations(request):
    from products.models import FinancialProduct, ProductOption

    user = request.user
    profile = getattr(user, 'profile', None)

    saving_style = request.data.get('saving_style', 'unknown')
    product_type = request.data.get('product_type', 'auto')
    preferred_term = request.data.get('preferred_term', '12')
    main_bank = request.data.get('main_bank', '없음')
    bank_filter = request.data.get('bank_filter', 'all')
    condition_preference = request.data.get('condition_preference', 'unknown')
    join_preference = request.data.get('join_preference', 'any')

    # 프론트에서 주거래은행을 '없음'으로 보낸 경우, 마이페이지 프로필 주거래은행 사용
    if main_bank in ['', None, '없음'] and profile:
        main_bank = profile.main_bank or '없음'

    # 저축 방식으로 상품 유형 자동 결정
    target_types = []

    if product_type == 'deposit':
        target_types = ['deposit']
    elif product_type == 'saving':
        target_types = ['saving']
    else:
        if saving_style == 'lump':
            target_types = ['deposit']
        elif saving_style == 'monthly':
            target_types = ['saving']
        else:
            target_types = ['deposit', 'saving']

    options = ProductOption.objects.select_related(
        'product',
        'product__bank'
    ).filter(
        product__product_type__in=target_types,
        intr_rate2__isnull=False,
    )

    # 기간 필터
    if preferred_term != 'any':
        try:
            term = int(preferred_term)
            options = options.filter(save_trm=term)
        except ValueError:
            term = None
    else:
        term = None

    # 주거래은행 상품만 보기
    if bank_filter == 'main_bank_only':
        if main_bank in ['', None, '없음']:
            return Response(
                {
                    'message': '주거래은행 상품만 보려면 주거래은행 정보가 필요합니다.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        options = options.filter(product__bank__name__icontains=normalize_bank_name(main_bank))

    candidates = []

    user_age = profile.age if profile else None
    user_gender = profile.gender if profile else 'unknown'

    for option in options:
        product = option.product

        age_eligibility = check_product_age_eligibility(product, user_age)

        if not age_eligibility['eligible']:
            continue

        gender_eligibility = check_product_gender_eligibility(product, user_gender)

        if not gender_eligibility['eligible']:
            continue

        score, reasons, condition_label, effective_rate = calculate_product_score(
            product=product,
            option=option,
            profile=profile,
            saving_style=saving_style,
            preferred_term=term,
            main_bank=main_bank,
            bank_filter=bank_filter,
            condition_preference=condition_preference,
            join_preference=join_preference,
        )

        candidates.append({
            'product_id': product.id,
            'option_id': option.id,
            'bank_name': product.bank.name,
            'product_name': product.name,
            'product_type': product.product_type,
            'product_type_label': '예금' if product.product_type == 'deposit' else '적금',
            'save_trm': option.save_trm,
            'base_rate': option.intr_rate or 0,
            'max_rate': option.intr_rate2 or option.intr_rate or 0,
            'effective_rate': effective_rate,
            'score': score,
            'condition_label': condition_label,
            'condition_description': product.spcl_cnd or '별도 우대조건 정보가 없습니다.',
            'join_way': product.join_way,
            'join_member': product.join_member,
            'eligibility_label': age_eligibility['label'],
            'eligibility_reason': age_eligibility['reason'],
            'eligibility_rule': age_eligibility['rule_description'],
            'gender_eligibility_label': gender_eligibility['label'],
            'gender_eligibility_reason': gender_eligibility['reason'],
            'gender_eligibility_rule': gender_eligibility['rule_description'],
            'reasons': reasons,
        })

    candidates.sort(
        key=lambda item: (
            item['score'],
            item['effective_rate'],
            item['max_rate'],
        ),
        reverse=True
    )

    return Response({
        'recommendations': candidates[:5],
        'profile_used': serialize_recommendation_profile(profile),
    })


def normalize_bank_name(bank_name):
    if not bank_name:
        return ''

    return (
        bank_name
        .replace('KB', '')
        .replace('NH', '')
        .replace(' ', '')
    )


def calculate_product_score(
    product,
    option,
    profile,
    saving_style,
    preferred_term,
    main_bank,
    bank_filter,
    condition_preference,
    join_preference,
):
    score = 0
    reasons = []

    base_rate = option.intr_rate or 0
    max_rate = option.intr_rate2 or option.intr_rate or 0
    effective_rate = max_rate

    # 1. 금리 점수
    score += float(base_rate) * 8
    score += float(max_rate) * 12

    if max_rate:
        reasons.append(f'최고 금리 {max_rate}% 조건을 가진 상품입니다.')

    # 2. 기간 일치
    if preferred_term and option.save_trm == preferred_term:
        score += 20
        reasons.append(f'희망 저축 기간인 {preferred_term}개월 조건과 일치합니다.')

    # 3. 저축 방식 일치
    if saving_style == 'lump' and product.product_type == 'deposit':
        score += 15
        reasons.append('목돈을 한 번에 예치하려는 방식에 맞는 예금 상품입니다.')

    if saving_style == 'monthly' and product.product_type == 'saving':
        score += 15
        reasons.append('매달 저축하는 방식에 맞는 적금 상품입니다.')

    # 4. 주거래은행 반영
    normalized_main_bank = normalize_bank_name(main_bank)
    normalized_product_bank = normalize_bank_name(product.bank.name)

    if normalized_main_bank and normalized_main_bank != '없음':
        if normalized_main_bank in normalized_product_bank or normalized_product_bank in normalized_main_bank:
            if bank_filter == 'main_bank_first':
                score += 25
            else:
                score += 15

            reasons.append(f'마이페이지 또는 추천 조건의 주거래은행인 {main_bank}과 연관된 상품입니다.')

    # 5. 가입 방식 반영
    join_way = product.join_way or ''

    if join_preference == 'online':
        if '인터넷' in join_way or '스마트폰' in join_way or '모바일' in join_way:
            score += 12
            reasons.append('인터넷/스마트폰 가입이 가능해 비대면 가입 선호에 맞습니다.')
    elif join_preference == 'branch':
        if '영업점' in join_way or '방문' in join_way:
            score += 12
            reasons.append('영업점 방문 가입 조건에 맞는 상품입니다.')

    # 6. 우대조건 선호 반영
    spcl_cnd = product.spcl_cnd or ''
    condition_label = '우대조건 확인 필요'

    if condition_preference == 'simple':
        simple_keywords = ['없음', '해당사항 없음', '제한없음', '조건 없음']
        hard_keywords = ['급여', '카드', '실적', '자동이체', '마케팅', '청약', '공과금']

        if any(keyword in spcl_cnd for keyword in simple_keywords):
            score += 18
            condition_label = '조건 단순'
            reasons.append('우대조건이 비교적 단순한 상품입니다.')
        elif not any(keyword in spcl_cnd for keyword in hard_keywords):
            score += 8
            condition_label = '조건 보통'
            reasons.append('복잡한 실적 조건이 상대적으로 적어 보이는 상품입니다.')
        else:
            score -= 8
            condition_label = '조건 복잡 가능'
    elif condition_preference == 'can_meet':
        if spcl_cnd:
            score += 8
            condition_label = '우대조건 활용 가능'
            reasons.append('우대조건을 맞출 수 있다면 최고금리를 노려볼 수 있습니다.')
    else:
        condition_label = '조건 확인 필요'

    # 7. 마이페이지 프로필 보조 점수
    if profile:
        if profile.monthly_saving_amount in ['under_10', '10_30'] and product.product_type == 'saving':
            score += 6
            reasons.append('월 저축 가능 금액을 고려하면 적금 방식이 부담이 적습니다.')

        if profile.lump_sum_amount not in ['', 'none'] and product.product_type == 'deposit':
            score += 6
            reasons.append('보유 목돈 정보를 고려하면 예금 상품도 검토할 수 있습니다.')

        if profile.personal_info_agree:
            score += 3

        age_eligibility = check_product_age_eligibility(product, profile.age)
        if age_eligibility.get('checked') and age_eligibility.get('rule_description'):
            reasons.append('마이페이지 나이 정보를 기준으로 가입대상 조건을 통과한 상품입니다.')

        gender_eligibility = check_product_gender_eligibility(product, profile.gender)
        if gender_eligibility.get('checked') and gender_eligibility.get('rule_description'):
            reasons.append('마이페이지 성별 정보를 기준으로 가입대상 조건을 통과한 상품입니다.')

    if not reasons:
        reasons.append('입력한 조건과 금리 정보를 종합해 추천한 상품입니다.')

    return round(score, 2), reasons[:4], condition_label, round(float(effective_rate), 2)


def serialize_recommendation_profile(profile):
    if not profile:
        return None

    return {
        'age': profile.age,
        'gender': profile.gender,
        'monthly_income_range': profile.monthly_income_range,
        'monthly_saving_amount': profile.monthly_saving_amount,
        'lump_sum_amount': profile.lump_sum_amount,
        'main_bank': profile.main_bank,
        'address': profile.address,
        'personal_info_agree': profile.personal_info_agree,
    }