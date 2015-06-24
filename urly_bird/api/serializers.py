from django.contrib.auth.models import User
from django.utils import timezone
from links.models import Bookmark, Click
from rest_framework import serializers
from hashids import Hashids


class ClickSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    bookmark = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Click

#######################################################################################################################

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    api_url = serializers.HyperlinkedIdentityField(view_name='bookmark-detail')
    code = serializers.SerializerMethodField()
    click_number = serializers.IntegerField(source='num_clicks', read_only=True)

    class Meta:
        model = Bookmark
        fields = ('id', 'api_url', 'code', 'url', 'title', 'description', 'timestamp', 'user', 'click_number')

    def get_code(self, obj):
        return obj.code

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(**validated_data)
        hashids = Hashids(salt="Hopefully the URLyBird does not get any worms")
        code = hashids.encode(bookmark.id)
        bookmark.code = code
        bookmark.save()
        return bookmark

#######################################################################################################################

class UserSerializer(serializers.HyperlinkedModelSerializer):
    total_clicks = serializers.IntegerField(source='num_clicks', read_only=True)
    bookmark_set = BookmarkSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'total_clicks', 'bookmark_set')