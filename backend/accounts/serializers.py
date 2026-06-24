from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserProfile


ALLOWED_GENDER_VALUES = {'unknown', 'male', 'female', ''}


def validate_gender_value(value):
    if value in [None, '']:
        return 'unknown'

    if value not in ALLOWED_GENDER_VALUES:
        raise serializers.ValidationError('성별 값을 확인해주세요.')

    return value

class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.',
            'blank': '아이디를 입력해주세요.',
        },
        validators=[]
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': '올바른 이메일 형식으로 입력해주세요.',
        }
    )

    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '비밀번호를 입력해주세요.',
            'blank': '비밀번호를 입력해주세요.',
        }
    )

    password_confirm = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '비밀번호 확인을 입력해주세요.',
            'blank': '비밀번호 확인을 입력해주세요.',
        }
    )

    age = serializers.IntegerField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True)
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
            'gender',
            'monthly_income_range',
            'monthly_saving_amount',
            'lump_sum_amount',
            'main_bank',
            'address',
            'personal_info_agree',
        )

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError('아이디를 입력해주세요.')

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('이미 존재하는 아이디입니다.')

        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError('이미 사용 중인 이메일입니다.')

        return value

    def validate_gender(self, value):
        return validate_gender_value(value)

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if not password:
            raise serializers.ValidationError({
                'message': '비밀번호를 입력해주세요.'
            })

        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': '비밀번호가 일치하지 않습니다.'
            })

        if data.get('personal_info_agree') is not True:
            raise serializers.ValidationError({
                'personal_info_agree': '개인정보 활용 동의가 필요합니다.'
            })

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        profile_data = {
            'age': validated_data.pop('age', None),
            'gender': validated_data.pop('gender', 'unknown') or 'unknown',
            'monthly_income_range': validated_data.pop('monthly_income_range', ''),
            'monthly_saving_amount': validated_data.pop('monthly_saving_amount', ''),
            'lump_sum_amount': validated_data.pop('lump_sum_amount', ''),
            'main_bank': validated_data.pop('main_bank', ''),
            'address': validated_data.pop('address', ''),
            'personal_info_agree': True,
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
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'profile_image',
            'profile_image_url',
            'age',
            'gender',
            'monthly_income_range',
            'monthly_saving_amount',
            'lump_sum_amount',
            'main_bank',
            'address',
            'personal_info_agree',
        )

    def get_profile_image_url(self, obj):
        if not obj.profile_image:
            return ''

        request = self.context.get('request')

        if request:
            return request.build_absolute_uri(obj.profile_image.url)

        return obj.profile_image.url


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'profile',
        )

    def get_profile(self, obj):
        profile, created = UserProfile.objects.get_or_create(user=obj)

        return UserProfileSerializer(
            profile,
            context=self.context
        ).data


class UserUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, allow_null=True)

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': '올바른 이메일 형식으로 입력해주세요.',
        }
    )
    age = serializers.IntegerField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True)
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
            'profile_image',
            'age',
            'gender',
            'monthly_income_range',
            'monthly_saving_amount',
            'lump_sum_amount',
            'main_bank',
            'address',
            'personal_info_agree',
        )

    def validate_email(self, value):
        request = self.context.get('request')
        current_user = request.user if request else None

        if value and User.objects.exclude(id=current_user.id).filter(email=value).exists():
            raise serializers.ValidationError('이미 사용 중인 이메일입니다.')

        return value

    def validate_gender(self, value):
        return validate_gender_value(value)

    def validate_personal_info_agree(self, value):
        if value is False:
            raise serializers.ValidationError('개인정보 활용 동의는 해제할 수 없습니다.')

        return value

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)

        if email is not None:
            instance.email = email
            instance.save()

        profile, created = UserProfile.objects.get_or_create(user=instance)

        profile_fields = [
            'profile_image',
            'age',
            'gender',
            'monthly_income_range',
            'monthly_saving_amount',
            'lump_sum_amount',
            'main_bank',
            'address',
        ]

        for field in profile_fields:
            if field in validated_data:
                setattr(profile, field, validated_data[field])

        if 'personal_info_agree' in validated_data:
            profile.personal_info_agree = True

        profile.save()

        return instance
    
class FindUsernameSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.',
            'blank': '이메일을 입력해주세요.',
            'invalid': '올바른 이메일 형식으로 입력해주세요.',
        }
    )

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value, is_active=True).exists():
            raise serializers.ValidationError('해당 이메일로 가입된 계정이 없습니다.')

        return value


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.',
            'blank': '아이디를 입력해주세요.',
        }
    )
    email = serializers.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.',
            'blank': '이메일을 입력해주세요.',
            'invalid': '올바른 이메일 형식으로 입력해주세요.',
        }
    )
    new_password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '새 비밀번호를 입력해주세요.',
            'blank': '새 비밀번호를 입력해주세요.',
        }
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '새 비밀번호 확인을 입력해주세요.',
            'blank': '새 비밀번호 확인을 입력해주세요.',
        }
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')

        try:
            user = User.objects.get(
                username=username,
                email__iexact=email,
                is_active=True
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'message': '아이디와 이메일이 일치하는 계정을 찾을 수 없습니다.'
            })

        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                'new_password_confirm': '새 비밀번호가 일치하지 않습니다.'
            })

        validate_password(new_password, user)

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '현재 비밀번호를 입력해주세요.',
            'blank': '현재 비밀번호를 입력해주세요.',
        }
    )
    new_password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '새 비밀번호를 입력해주세요.',
            'blank': '새 비밀번호를 입력해주세요.',
        }
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '새 비밀번호 확인을 입력해주세요.',
            'blank': '새 비밀번호 확인을 입력해주세요.',
        }
    )

    def validate(self, data):
        request = self.context.get('request')
        user = request.user

        if not user.check_password(data.get('current_password')):
            raise serializers.ValidationError({
                'current_password': '현재 비밀번호가 올바르지 않습니다.'
            })

        if data.get('new_password') != data.get('new_password_confirm'):
            raise serializers.ValidationError({
                'new_password_confirm': '새 비밀번호가 일치하지 않습니다.'
            })

        validate_password(data.get('new_password'), user)

        return data

    def save(self):
        request = self.context.get('request')
        user = request.user

        user.set_password(self.validated_data['new_password'])
        user.save()

        return user


class WithdrawSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '비밀번호를 입력해주세요.',
            'blank': '비밀번호를 입력해주세요.',
        }
    )

    def validate_password(self, value):
        request = self.context.get('request')
        user = request.user

        if not user.check_password(value):
            raise serializers.ValidationError('비밀번호가 올바르지 않습니다.')

        return value