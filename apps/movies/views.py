from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from apps.movies.forms import SearchForm
from django.views.generic.edit import FormView

from apps.movies.models import Movie, Actor


class SearchFormView(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.search:
            context['movies'] = Movie.objects.filter(name__icontains=self.search)
            context['actors'] = Actor.objects.filter(name__icontains=self.search)
            context['search'] = self.search
        return context

    def get(self, *args, search=None, **kwargs):
        self.search = search
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('movies:search', kwargs={'search': form.cleaned_data['search']}))


class MovieView(DetailView):
    template_name = 'movie_detail.html'

    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actors'] = self.object.actors.all()
        return context


class ActorView(DetailView):
    template_name = 'actor_detail.html'

    model = Actor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = self.object.movies.all()
        return context
