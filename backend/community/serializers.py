from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
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
            'like_count',
            'is_liked',
            'is_author',
            'created_at',
        )

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
            'view_count',
            'comment_count',
            'like_count',
            'is_liked',
            'is_author',
            'created_at',
            'updated_at',
        )

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
            'view_count',
            'like_count',
            'is_liked',
            'is_author',
            'comments',
            'created_at',
            'updated_at',
        )

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