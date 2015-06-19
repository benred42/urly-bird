from django import forms
from links.models import Bookmark
from django.utils import timezone



class BookmarkForm(forms.ModelForm):
    url = forms.URLField()
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    code = forms.CharField(widget=forms.HiddenInput(), required=False)
    timestamp = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now)

    class Meta:
        model = Bookmark
        fields = ("url", "title", "description", "code", "timestamp")


class EditBookmarkForm(BookmarkForm):
    code = forms.CharField()
