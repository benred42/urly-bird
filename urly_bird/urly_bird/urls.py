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
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/nest/')),
    url(r'^nest/$', link_views.AllBookmarksList.as_view(), name="all_bookmarks"),
    url(r'^nest/(?P<user_id>\d+)$', link_views.UserBookmarksList.as_view(), name="user_bookmarks"),
    url(r'^nest/egg/new/(?P<return_url>.*)?$', link_views.CreateBookmark.as_view(), name="create_bookmark"),
    url(r'^nest/egg/edit/(?P<pk>\d*)/(?P<return_url>.*)?$', link_views.EditBookmark.as_view(), name="edit_bookmark"),
    url(r'^nest/egg/delete/(?P<pk>\d*)/(?P<return_url>.*)?$', link_views.DeleteBookmark.as_view(), name="delete_bookmark"),
    url(r'^egg/(?P<code>\w+)$', link_views.BookmarkRedirect.as_view(), name='bookmark_redirect'),
    url(r'^login/$', builtin.login, name="login"),
    url(r'^logout/', builtin.logout_then_login, {"login_url": "login"}, name="logout"),
    url(r'^register/$', account_views.register_rater, name="user_register"),
]
