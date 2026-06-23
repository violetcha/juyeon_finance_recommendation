from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    MONTHLY_INCOME_CHOICES = [
        ('under_100', '100만원 미만'),
        ('100_200', '100만원 이상 200만원 미만'),
        ('200_300', '200만원 이상 300만원 미만'),
        ('300_400', '300만원 이상 400만원 미만'),
        ('400_500', '400만원 이상 500만원 미만'),
        ('over_500', '500만원 이상'),
    ]

    MONTHLY_SAVING_CHOICES = [
        ('under_10', '10만원 미만'),
        ('10_30', '10만원 이상 30만원 미만'),
        ('30_50', '30만원 이상 50만원 미만'),
        ('50_100', '50만원 이상 100만원 미만'),
        ('over_100', '100만원 이상'),
    ]

    LUMP_SUM_CHOICES = [
        ('none', '없음'),
        ('under_100', '100만원 미만'),
        ('100_500', '100만원 이상 500만원 미만'),
        ('500_1000', '500만원 이상 1000만원 미만'),
        ('1000_3000', '1000만원 이상 3000만원 미만'),
        ('over_3000', '3000만원 이상'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True
    )


    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    monthly_income_range = models.CharField(
        max_length=20,
        choices=MONTHLY_INCOME_CHOICES,
        blank=True
    )

    monthly_saving_amount = models.CharField(
        max_length=20,
        choices=MONTHLY_SAVING_CHOICES,
        blank=True
    )

    lump_sum_amount = models.CharField(
        max_length=20,
        choices=LUMP_SUM_CHOICES,
        blank=True
    )

    main_bank = models.CharField(
        max_length=50,
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    personal_info_agree = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.user.username} 금융 프로필'