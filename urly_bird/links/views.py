from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, RedirectView, CreateView, UpdateView, DeleteView
from links.forms import BookmarkForm, EditBookmarkForm
from links.models import Bookmark, Click
from django.utils import timezone
from hashids import Hashids

# Create your views here.
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AllBookmarksList(ListView):
    model = Bookmark
    context_object_name = "bookmarks"
    template_name = "links/all_bookmarks.html"
    queryset = Bookmark.objects.all().order_by("-timestamp")
    paginate_by = 20


class UserBookmarksList(ListView):
    model = Bookmark
    context_object_name = "bookmarks"
    template_name = "links/user_bookmarks.html"
    paginate_by = 20

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Bookmark.objects.filter(user=get_object_or_404(User, pk=user_id)).order_by("-timestamp").select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs["user_id"]
        context["user"] = get_object_or_404(User, pk=user_id)
        return context


class BookmarkRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        bookmark = get_object_or_404(Bookmark, code=kwargs['code'])
        click = Click(user=self.request.user,
                      bookmark=bookmark,
                      timestamp=timezone.now())
        click.save()
        return bookmark.url


class CreateBookmark(LoginRequiredMixin, CreateView):
    model = Bookmark
    form_class = BookmarkForm
    template_name = "links/new_bookmark.html"

    def form_valid(self, form):
        self.request.return_url = self.request.path
        form.instance = form.save(commit=False)
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             "Your link has been successfully bookmarked!")
        return super().form_valid(form)

    def get_success_url(self):
        hashids = Hashids(salt="Hopefully the URLyBird does not get any worms")
        self.object.code = hashids.encode(self.object.id)
        self.object.save()
        return_url = self.request.GET.get('return_url', '')
        return return_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return_url = self.request.GET['return_url']
        context["return_url"] = return_url
        return context


class EditBookmark(LoginRequiredMixin, UpdateView):
    model = Bookmark
    form_class = EditBookmarkForm
    template_name = "links/edit_bookmark.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context["pk"] = pk
        return_url = self.request.GET['return_url']
        context["return_url"] = return_url
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Your bookmark has been successfully updated!")
        return_url = self.request.GET.get('return_url', '')
        return return_url


class DeleteBookmark(LoginRequiredMixin, DeleteView):
    model = Bookmark
    template_name = "links/delete_bookmark.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        context["pk"] = pk
        return_url = self.request.GET['return_url']
        context["return_url"] = return_url
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Your bookmark has been successfully deleted!")
        return_url = self.request.GET.get('return_url', '')
        return return_url
