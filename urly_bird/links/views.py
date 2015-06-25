from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, RedirectView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.views.generic.list import MultipleObjectMixin
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
    queryset = Bookmark.objects.all().order_by("-timestamp").select_related()
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
        if not self.request.user.is_anonymous():
            click = Click(user=self.request.user,
                          bookmark=bookmark,
                          timestamp=timezone.now())
        else:
            click = Click(user=User.objects.get(pk=103),
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


class BookmarkStats(TemplateView):
    template_name = "links/bookmark_stats.html"
    context_object_name = "bookmarks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookmark_id = self.kwargs["bookmark_id"]
        context['bookmark'] = get_object_or_404(Bookmark, pk=bookmark_id)
        return context


class UserStats(LoginRequiredMixin, ListView):
    template_name = "links/user_stats.html"
    context_object_name = "bookmarks"
    paginate_by = 10

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).annotate(num=Count('click')).order_by('-num')


class SearchBookmarks(ListView):
    model = Bookmark
    template_name = 'links/search_bookmarks.html'
    context_object_name = "results_bookmarks"
    paginate_by = 10

    def get_queryset(self):
        search_input = self.request.GET.get('search_bookmarks')
        return Bookmark.objects.all().filter(title__icontains=search_input)


class SearchUsers(ListView):
    model = User
    template_name = 'links/search_users.html'
    context_object_name = "results_users"
    paginate_by = 10

    def get_queryset(self):
        search_input = self.request.GET.get('search_users')
        return User.objects.all().filter(username__icontains=search_input)


# class SearchUsers(View):
#     def post(self, request):
#         if request.method == "POST":
#             search_input = request.POST.get('search_users')
#             results = User.objects.all()
#             if search_input:
#                 results_users = results.filter(username__icontains=search_input)
#                 return render(request,
#                               'links/search_users.html',
#                               {'results_users': results_users})
#         return render(request,
#                       'links/search_users.html',
#                       {'results_users': None})

#######################################################################################################################

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib

matplotlib.style.use('ggplot')


def bookmark_chart(request, bookmark_id):
    clicks = Click.objects.filter(bookmark__id=bookmark_id).filter(timestamp__gte=timezone.now() - timedelta(days=30))
    df = pd.DataFrame(model_to_dict(click) for click in clicks)
    # df = pd.DataFrame(click.to_dict() for click in clicks)
    df.index = df['timestamp']
    df['count'] = 1
    counts = df['count']
    counts = counts.sort_index()
    series = counts.resample('D', how=sum, fill_method='pad')
    response = HttpResponse(content_type='image/png')

    fig = plt.figure(figsize=(10, 4))
    fig.patch.set_alpha(0)
    plt.plot(series.index, series.values)
    ymin, ymax = plt.ylim()
    plt.ylim((ymin - 1), (ymax + 1))
    plt.xticks(size=7)
    plt.xlabel("")
    plt.ylabel("Number of Clicks")
    canvas = FigureCanvas(fig)
    canvas.print_png(response)
    return response


def user_chart(request):
    clicks = Click.objects.filter(user=request.user).filter(timestamp__gte=timezone.now() - timedelta(days=30))
    df = pd.DataFrame(model_to_dict(click) for click in clicks)
    # df = pd.DataFrame(click.to_dict() for click in clicks)
    df.index = df['timestamp']
    df['count'] = 1
    counts = df['count']
    counts = counts.sort_index()
    series = counts.resample('D', how=sum, fill_method='pad')
    response = HttpResponse(content_type='image/png')

    fig = plt.figure(figsize=(10, 4))
    fig.patch.set_alpha(0)
    plt.plot(series.index, series.values)
    ymin, ymax = plt.ylim()
    plt.ylim((ymin - 1), (ymax + 1))
    plt.xticks(size=7)
    plt.xlabel("")
    plt.ylabel("Number of Clicks")
    canvas = FigureCanvas(fig)
    canvas.print_png(response)
    return response
