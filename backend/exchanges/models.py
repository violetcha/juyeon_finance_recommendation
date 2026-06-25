from django.db import models


class ExchangeRate(models.Model):
    """한국수출입은행 환율 데이터를 DB에 저장하기 위한 모델.

    예적금 상품과 같은 흐름으로 사용한다.
    - API 조회 성공 시 DB에 저장
    - 이후 화면 응답은 DB 데이터 기준으로 반환
    - API 장애 시 fixture로 넣어둔 DB 데이터를 사용
    """

    date = models.DateField(db_index=True)
    currency_code = models.CharField(max_length=20)
    normalized_code = models.CharField(max_length=10, db_index=True)
    currency_name = models.CharField(max_length=60)

    # raw_rate: API 원본 기준 환율. 예) USD=1538.3, JPY(100)=950.92
    raw_rate = models.DecimalField(max_digits=16, decimal_places=4)

    # rate_per_unit: 계산용 1단위 기준 환율. 예) USD=1538.3, JPY=9.5092
    rate_per_unit = models.DecimalField(max_digits=16, decimal_places=6)

    unit = models.PositiveSmallIntegerField(default=1)
    display_unit = models.CharField(max_length=20)
    source = models.CharField(max_length=30, default='fixture')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'normalized_code']
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'normalized_code'],
                name='unique_exchange_rate_by_date_currency',
            ),
        ]

    def __str__(self):
        return f'{self.date} {self.normalized_code} {self.raw_rate}'
