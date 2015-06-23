from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, permissions, generics
from api.serializers import BookmarkSerializer, ClickSerializer
from links.models import Bookmark
from api.permissions import IsOwnerOrReadOnly
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all().annotate(num_clicks=Count('click'))
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
