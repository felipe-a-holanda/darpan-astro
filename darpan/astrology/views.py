
from django.shortcuts import render
from django.views import generic

from .models import *
from posts.models import Post

class AstroListView(generic.ListView):
    model = AstroChart

class AstroDetailView(generic.DetailView):
    model = AstroChart

class AstroPlanetSign(generic.ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = 'astrology'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tags__name__in=['astrology'])
        return queryset
