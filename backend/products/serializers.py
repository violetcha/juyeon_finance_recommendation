from rest_framework import serializers
from .models import Bank, FinancialProduct, ProductOption


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('id', 'name', 'code')


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = (
            'id',
            'intr_rate_type',
            'intr_rate_type_nm',
            'rsrv_type',
            'rsrv_type_nm',
            'intr_rate',
            'intr_rate2',
        )


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = [
            'id',
            'name',
            'code',
        ]


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = [
            'id',
            'intr_rate_type',
            'intr_rate_type_nm',
            'rsrv_type',
            'rsrv_type_nm',
            'save_trm',
            'intr_rate',
            'intr_rate2',
        ]


class FinancialProductListSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    options = ProductOptionSerializer(many=True, read_only=True)
    max_interest_rate = serializers.SerializerMethodField()

    class Meta:
        model = FinancialProduct
        fields = [
            'id',
            'bank',
            'product_type',
            'fin_prdt_cd',
            'name',
            'join_way',
            'join_member',
            'max_interest_rate',
            'options',
        ]

    def get_max_interest_rate(self, obj):
        rates = []

        for option in obj.options.all():
            if option.intr_rate2 is not None:
                rates.append(option.intr_rate2)
            elif option.intr_rate is not None:
                rates.append(option.intr_rate)

        if not rates:
            return None

        return max(rates)


class FinancialProductDetailSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    options = ProductOptionSerializer(many=True, read_only=True)
    max_interest_rate = serializers.SerializerMethodField()

    class Meta:
        model = FinancialProduct
        fields = [
            'id',
            'bank',
            'product_type',
            'fin_prdt_cd',
            'name',
            'join_way',
            'mtrt_int',
            'spcl_cnd',
            'join_deny',
            'join_member',
            'etc_note',
            'max_limit',
            'dcls_month',
            'dcls_strt_day',
            'dcls_end_day',
            'fin_co_subm_day',
            'max_interest_rate',
            'options',
        ]

    def get_max_interest_rate(self, obj):
        rates = []

        for option in obj.options.all():
            if option.intr_rate2 is not None:
                rates.append(option.intr_rate2)
            elif option.intr_rate is not None:
                rates.append(option.intr_rate)

        if not rates:
            return None

        return max(rates)