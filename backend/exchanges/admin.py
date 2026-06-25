from django.contrib import admin

from .models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'normalized_code',
        'currency_name',
        'raw_rate',
        'rate_per_unit',
        'display_unit',
        'source',
    )
    list_filter = ('date', 'normalized_code', 'source')
    search_fields = ('currency_code', 'normalized_code', 'currency_name')
    ordering = ('-date', 'normalized_code')
