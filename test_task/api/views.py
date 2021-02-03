from .models import *
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    action_serializers = {
        'retrieve': BlogDetailSerializer,
        'list': BlogListSerializer,
        'create': BlogDetailSerializer
    }

    # Choose appropriate serializer from action_serializers dictionary based on action
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(BlogViewSet, self).get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
