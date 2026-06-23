from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    age = serializers.IntegerField(required=False, allow_null=True)
    monthly_income_range = serializers.CharField(required=False, allow_blank=True)
    monthly_saving_amount = serializers.CharField(required=False, allow_blank=True)
    lump_sum_amount = serializers.CharField(required=False, allow_blank=True)
    main_bank = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    personal_info_agree = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'password_confirm',
            'email',
            'age',
            'monthly_income_range',
            'monthly_saving_amount',
            'lump_sum_amount',
            'main_bank',
            'address',
            'personal_info_agree',
        )

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        profile_data = {
            'age': validated_data.pop('age', None),
            'monthly_income_range': validated_data.pop('monthly_income_range', ''),
            'monthly_saving_amount': validated_data.pop('monthly_saving_amount', ''),
            'lump_sum_amount': validated_data.pop('lump_sum_amount', ''),
            'main_bank': validated_data.pop('main_bank', ''),
            'address': validated_data.pop('address', ''),
            'personal_info_agree': validated_data.pop('personal_info_agree', False),
        }

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )

        UserProfile.objects.create(
            user=user,
            **profile_data
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'age',
            'monthly_income_range',
            'monthly_saving_amount',
            'lump_sum_amount',
            'main_bank',
            'address',
            'personal_info_agree',
        )


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'profile',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False, allow_null=True)
    monthly_income_range = serializers.CharField(required=False, allow_blank=True)
    monthly_saving_amount = serializers.CharField(required=False, allow_blank=True)
    lump_sum_amount = serializers.CharField(required=False, allow_blank=True)
    main_bank = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    personal_info_agree = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'age',
            'monthly_income_range',
            'monthly_saving_amount',
            'lump_sum_amount',
            'main_bank',
            'address',
            'personal_info_agree',
        )

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)

        if email is not None:
            instance.email = email
            instance.save()

        profile, created = UserProfile.objects.get_or_create(user=instance)

        profile_fields = [
            'age',
            'monthly_income_range',
            'monthly_saving_amount',
            'lump_sum_amount',
            'main_bank',
            'address',
            'personal_info_agree',
        ]

        for field in profile_fields:
            if field in validated_data:
                setattr(profile, field, validated_data[field])

        profile.save()

        return instance
    
