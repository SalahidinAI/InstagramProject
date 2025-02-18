from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'save', SaveViewSet, basename='save_list')
router.register(r'save_item', SaveItemViewSet, basename='save_list')

urlpatterns = [
    path('', include(router.urls)),
    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileEditAPIView.as_view(), name='user_edit'),

    path('post/', PostListAPIView.as_view(), name='post_list'),
    path('post/create/', PostCreateAPIView.as_view(), name='post_create'),
    path('post_list/', PostOwnerListAPIView.as_view(), name='post_owner_list'),
    path('post_list/<int:pk>/', PostOwnerEditAPIView.as_view(), name='post_owner_list'),

    path('follow/', FollowListAPIView.as_view(), name='follow_list'),
    path('follow/create/', FollowCreateAPIView.as_view(), name='follow_create'),
    path('follow/<int:pk>/', FollowEditAPIView.as_view(), name='follow_edit'),

    path('post_like/create/', PostLikeCreateAPIView.as_view(), name='post_like_create'),
    path('comment/create/', CommentCreateAPIView.as_view(), name='comment_create'),
    path('comment_like/create/', CommentLikeCreateAPIView.as_view(), name='comment_like_create'),

    path('story/', StoryListAPIView.as_view(), name='story_list'),
    path('story/create/', StoryCreateAPIView.as_view(), name='story_create'),
    path('story_list/', StoryOwnerListAPIView.as_view(), name='story_owner_list'),
    path('story_list/<int:pk>/', StoryOwnerEditAPIView.as_view(), name='story_owner_edit'),
]
