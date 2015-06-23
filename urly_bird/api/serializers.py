from links.models import Bookmark
from rest_framework import serializers


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Bookmark
        fields = ('id', 'url', "URL", 'code', 'title', 'description', 'timestamp', 'user')