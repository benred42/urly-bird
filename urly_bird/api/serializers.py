from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from links.models import Bookmark, Click
from rest_framework import serializers
from hashids import Hashids
from rest_framework.reverse import reverse


class ClickSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    bookmark = serializers.PrimaryKeyRelatedField(read_only=True)
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Click

    def create(self, validated_data):
        """Automatically sets the timestamp for a bookmark."""
        click = Click.objects.create(**validated_data)
        click.timestamp = timezone.now()
        click.save()
        return click


    def get_timestamp(self, obj):
        return obj.timestamp


#######################################################################################################################

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    api_url = serializers.HyperlinkedIdentityField(view_name='bookmark-detail')
    code = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    click_number = serializers.IntegerField(source='num_clicks', read_only=True)
    click_count = serializers.SerializerMethodField()
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = (
            'id', 'api_url', 'code', 'url', 'title', 'description', 'timestamp', 'user', 'click_number', 'click_count',
            '_links')

    def get_code(self, obj):
        return obj.code

    def get_timestamp(self, obj):
        return obj.timestamp

    def get__links(self, obj):
        links = {
            "clicks": reverse('create_click', kwargs=dict(bookmark_id=obj.id),
                              request=self.context.get('request'))}
        return links

    def get_click_count(self, obj):
        bookmark = Bookmark.objects.filter(pk=obj.id).annotate(click_num=Count('click'))
        return bookmark[0].click_num

    def create(self, validated_data):
        """Automatically sets the short url code and the timestamp for a bookmark."""
        bookmark = Bookmark.objects.create(**validated_data)
        hashids = Hashids(salt="Hopefully the URLyBird does not get any worms")
        code = hashids.encode(bookmark.id)
        bookmark.code = code
        bookmark.timestamp = timezone.now()
        bookmark.save()
        return bookmark


#######################################################################################################################

class UserSerializer(serializers.HyperlinkedModelSerializer):
    total_clicks = serializers.IntegerField(source='num_clicks', read_only=True)
    bookmark_set = BookmarkSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'total_clicks', 'bookmark_set', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        user = authenticate(username=user.username,
                            password=validated_data['password'])

        login(self.context.get('request'), user)

        return user
