from django.shortcuts import render
from rest_framework import viewsets, permissions
from api.serializers import BookmarkSerializer
from links.models import Bookmark
from api.permissions import IsOwnerOrReadOnly


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
