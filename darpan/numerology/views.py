from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from posts.models import Post
from .models import NumerologyChart

from numerology.forms import PostNumerologyForm

class NumerologyDetailView(DetailView):

    model = NumerologyChart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = timezone.now()
        return context



class PostListView(ListView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = []
        if 'tag' in self.kwargs:
            tags.append(self.kwargs['tag'])
        if 'tag2' in self.kwargs:
            tags.append(self.kwargs['tag2'])
        context['current_tags'] = tags
        context['form'] = PostNumerologyForm()
        context['users'] = NumerologyChart.objects.filter(tags__name__in=tags)
        return context
    
    def get_queryset(self):
        
        posts = Post.objects.filter(tags__name__in=['numerology'])
        
        if 'tag' in self.kwargs:
            tag = self.kwargs['tag']
            posts = posts.filter(tags__name__in=[tag])
        if 'tag2' in self.kwargs:
            tag = self.kwargs['tag2']
            posts = posts.filter(tags__name__in=[tag])
        return posts






class PostCreate(CreateView):
    model = Post
    fields = ['title', 'text', 'source', 'tags']
    
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        tags = form.cleaned_data['tags']
        tags.append('numerology')
        if 'tag' in self.kwargs:
            tags.append(self.kwargs['tag'])
        form.cleaned_data['tags'] = tags
        
        return super().form_valid(form)



class PostListFormView(View):

    def get(self, request, *args, **kwargs):
        view = PostListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCreate.as_view()
        return view(request, *args, **kwargs)
