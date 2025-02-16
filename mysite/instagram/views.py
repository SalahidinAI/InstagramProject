from .models import *
from .serializers import *
from .permissions import *
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import TwoPagination
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class UserProfileEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [CheckUserProfileEdit]


class FollowCreateAPIView(generics.CreateAPIView):
    serializer_class = FollowSerializer


class FollowListAPIView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer

    def get_queryset(self):
        return Follow.objects.filter(
            Q(follower=self.request.user) |
            Q(following=self.request.user)
        )


class FollowEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [CheckFollowEdit]


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'hashtag']
    search_fields = ['user__username']
    ordering_fields = ['created_at']
    pagination_class = TwoPagination


class PostOwnerListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = TwoPagination

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class PostOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [CheckOwnerEdit]


class PostLikeCreateAPIView(generics.CreateAPIView):
    serializer_class = PostLikeSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer


class CommentLikeCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentLikeSerializer


class StoryCreateAPIView(generics.CreateAPIView):
    serializer_class = StorySerializer


class StoryListAPIView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryListSerializer


class StoryOwnerListAPIView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryListSerializer

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)


class StoryOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [CheckOwnerEdit]


class SaveViewSet(viewsets.ModelViewSet):
    queryset = Saves.objects.all()
    serializer_class = SaveSerializer

    def get_queryset(self):
        return Saves.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        saves, created = Saves.objects.get_or_create(user=self.request.user)
        serializers = self.get_serializer(saves)
        return Response(serializers.data)


class SaveItemViewSet(viewsets.ModelViewSet):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemSerializer

    def get_queryset(self):
        return SaveItem.objects.filter(save_cart__user=self.request.user)

    def perform_create(self, serializer):
        save_cart, created = Saves.objects.get_or_create(user=self.request.user)
        serializer.save(save_cart=save_cart)
