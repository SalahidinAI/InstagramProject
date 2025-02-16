from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name',
                  'user_image','bio', 'website')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileListSerializer(serializers.ModelSerializer):
    post_quantity = serializers.SerializerMethodField()
    following_quantity = serializers.SerializerMethodField()
    follower_quantity = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'bio',
                  'user_image', 'website', 'post_quantity',
                  'following_quantity', 'follower_quantity']

    def get_post_quantity(self, obj):
        return obj.get_post_quantity()

    def get_following_quantity(self, obj):
        return obj.get_following_quantity()

    def get_follower_quantity(self, obj):
        return obj.get_follower_quantity()


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class FollowListSerializer(serializers.ModelSerializer):
    follower = UserProfileSimpleSerializer()
    following = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format='%d %B %Y %H:%M')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    likes_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user', 'text', 'parent', 'created_at', 'likes_quantity']

    def get_likes_quantity(self, obj):
        return obj.get_likes_quantity()


class PostListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format='%d %B %y %H:%M')
    like_quantity = serializers.SerializerMethodField()
    post_comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'post_image', 'video', 'description', 'hashtag',
                  'created_at', 'like_quantity', 'post_comments']

    def get_like_quantity(self, obj):
        return obj.get_like_quantity()


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class StoryListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Story
        fields = ['id', 'user', 'image', 'video', 'created_at']


class SaveItemSerializer(serializers.ModelSerializer):
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True, source='post')
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = SaveItem
        fields = ['id', 'save_cart', 'post_id', 'post', 'created_date']


class SaveSerializer(serializers.ModelSerializer):
    saved_items = SaveItemSerializer(many=True, read_only=True)

    class Meta:
        model = Saves
        fields = ['id', 'user', 'saved_items']
