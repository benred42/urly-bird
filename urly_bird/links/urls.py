from django.conf.urls import include, url
from links import views as link_views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/nest/')),
    url(r'^nest/$', link_views.AllBookmarksList.as_view(), name="all_bookmarks"),
    url(r'^nest/(?P<user_id>\d+)$', link_views.UserBookmarksList.as_view(), name="user_bookmarks"),
    url(r'^nest/egg/(?P<bookmark_id>\d+)$', link_views.BookmarkStats.as_view(), name="bookmark_stats"),
    url(r'^bookmarks.png/(?P<bookmark_id>\d*)?$', link_views.bookmark_chart, name="bookmark_chart"),
    url(r'^nest/stats/$', link_views.UserStats.as_view(), name="user_stats"),
    url(r'^clicks.png/$', link_views.user_chart, name="user_chart"),
    url(r'^nest/egg/new/(?P<return_url>.*)?$', link_views.CreateBookmark.as_view(), name="create_bookmark"),
    url(r'^nest/egg/edit/(?P<pk>\d*)/(?P<return_url>.*)?$', link_views.EditBookmark.as_view(), name="edit_bookmark"),
    url(r'^nest/egg/delete/(?P<pk>\d*)/(?P<return_url>.*)?$', link_views.DeleteBookmark.as_view(),
        name="delete_bookmark"),
    url(r'^egg/(?P<code>\w+)$', link_views.BookmarkRedirect.as_view(), name='bookmark_redirect'),
    url(r'^results/eggs/$', link_views.SearchBookmarks.as_view(), name="search_bookmarks"),
    url(r'^results/birds/$', link_views.SearchUsers.as_view(), name="search_users"),
]
