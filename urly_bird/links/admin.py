from django.contrib import admin
from links.models import Bookmark, Click

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "url", "code", "timestamp", "user"]

# Register your models here.
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Click)
