"""urly_bird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as builtin
from accounts import views as account_views
from links import views as link_views
from api import views as api_views
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bookmarks', api_views.BookmarkViewSet)
router.register(r'user', api_views.UserViewSet, base_name="user")

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
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
    url(r'^login/$', builtin.login, name="login"),
    url(r'^logout/', builtin.logout_then_login, {"login_url": "login"}, name="logout"),
    url(r'^register/$', account_views.register_rater, name="user_register"),
    url(r'^results/eggs/$', link_views.SearchBookmarks.as_view(), name="search_bookmarks"),
    url(r'^results/birds/$', link_views.SearchUsers.as_view(), name="search_users"),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/bookmarks/(?P<bookmark_id>\d+)/click', api_views.ClickView.as_view(), name="create_click")
]
