# Generated manually for ExchangeRate DB cache and fixture fallback.

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('currency_code', models.CharField(max_length=20)),
                ('normalized_code', models.CharField(db_index=True, max_length=10)),
                ('currency_name', models.CharField(max_length=60)),
                ('raw_rate', models.DecimalField(decimal_places=4, max_digits=16)),
                ('rate_per_unit', models.DecimalField(decimal_places=6, max_digits=16)),
                ('unit', models.PositiveSmallIntegerField(default=1)),
                ('display_unit', models.CharField(max_length=20)),
                ('source', models.CharField(default='fixture', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date', 'normalized_code'],
            },
        ),
        migrations.AddConstraint(
            model_name='exchangerate',
            constraint=models.UniqueConstraint(fields=('date', 'normalized_code'), name='unique_exchange_rate_by_date_currency'),
        ),
    ]
