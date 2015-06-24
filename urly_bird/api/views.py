from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, permissions, generics
from api.serializers import BookmarkSerializer, ClickSerializer, UserSerializer
from links.models import Bookmark
from api.permissions import IsOwnerOrReadOnly, IsSameUser
from rest_framework.pagination import PageNumberPagination


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all().annotate(num_clicks=Count('click')).select_related()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClickView(generics.CreateAPIView):
    serializer_class = ClickSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        bookmark = Bookmark.objects.filter(pk=self.kwargs['bookmark_id'])[0]
        if self.request.user.is_authenticated():
            serializer.save(user=self.request.user, bookmark=bookmark)
        else:
            serializer.save(user=User.objects.get(pk=103), bookmark=bookmark)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSameUser)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = User.objects.all().annotate(num_clicks=Count('bookmark__click')).filter(
            pk=self.request.user.id).select_related()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
