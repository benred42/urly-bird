from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, permissions, generics, filters
from api.serializers import BookmarkSerializer, ClickSerializer, UserSerializer
from links.models import Bookmark, Click
from api.permissions import IsOwnerOrReadOnly, IsSameUser
import django_filters


class BookmarkFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(name="title", lookup_type="icontains")
    description = django_filters.CharFilter(name="description", lookup_type="icontains")
    user = django_filters.NumberFilter(name='user', lookup_type="exact")

    class Meta:
        model = Bookmark
        fields = ['title', 'description', 'user']


class BookmarkViewSet(viewsets.ModelViewSet):
    """Add the following search terms to the url to filter results:
    title=your+title+search
    description=your+description+search
    user=your+user+id+search
    Example: http://host/api/bookmarks/?title=nest&description=birds+live"""
    queryset = Bookmark.objects.all().annotate(num_clicks=Count('click'))
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BookmarkFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClickView(generics.ListCreateAPIView):
    serializer_class = ClickSerializer

    def get_queryset(self):
        return Click.objects.filter(bookmark__id=self.kwargs['bookmark_id'])

    def perform_create(self, serializer):
        bookmark = Bookmark.objects.filter(pk=self.kwargs['bookmark_id'])[0]
        if self.request.user.is_authenticated():
            serializer.save(user=self.request.user, bookmark=bookmark)
        else:
            serializer.save(user=User.objects.get(pk=103), bookmark=bookmark)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsSameUser,)

    def get_queryset(self):
        queryset = User.objects.all().annotate(num_clicks=Count('bookmark__click')).filter(
            pk=self.request.user.id)
        return queryset
