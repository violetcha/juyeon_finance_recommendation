from rest_framework import serializers
from .models import Post, Comment
from accounts.models import UserProfile



def get_profile_image_url(user, request=None):
    profile = UserProfile.objects.filter(user=user).first()

    if not profile or not profile.profile_image:
        return None

    image_url = profile.profile_image.url

    if request:
        return request.build_absolute_uri(image_url)

    return image_url


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_profile_image = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'post',
            'user',
            'user_id',
            'username',
            'user_profile_image',
            'content',
            'like_count',
            'is_liked',
            'is_author',
            'created_at',
        )
        read_only_fields = (
            'post',
            'user',
            'user_id',
            'username',
            'user_profile_image',
            'like_count',
            'is_liked',
            'is_author',
            'created_at',
        )

    def get_user_profile_image(self, obj):
        return get_profile_image_url(obj.user, self.context.get('request'))

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.likes.filter(id=request.user.id).exists()

    def get_is_author(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.user_id == request.user.id


class PostListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_profile_image = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'category',
            'user_id',
            'username',
            'user_profile_image',
            'view_count',
            'comment_count',
            'like_count',
            'is_liked',
            'is_author',
            'created_at',
            'updated_at',
        )

    def get_user_profile_image(self, obj):
        return get_profile_image_url(obj.user, self.context.get('request'))

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.likes.filter(id=request.user.id).exists()

    def get_is_author(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.user_id == request.user.id


class PostDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_profile_image = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'category',
            'user',
            'user_id',
            'username',
            'user_profile_image',
            'view_count',
            'like_count',
            'is_liked',
            'is_author',
            'comments',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'user',
            'user_id',
            'username',
            'user_profile_image',
            'view_count',
            'like_count',
            'is_liked',
            'is_author',
            'comments',
            'created_at',
            'updated_at',
        )

    def get_user_profile_image(self, obj):
        return get_profile_image_url(obj.user, self.context.get('request'))

    def get_comments(self, obj):
        comments = obj.comments.select_related('user').prefetch_related('likes').all()

        return CommentSerializer(
            comments,
            many=True,
            context=self.context,
        ).data

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.likes.filter(id=request.user.id).exists()

    def get_is_author(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return obj.user_id == request.user.id