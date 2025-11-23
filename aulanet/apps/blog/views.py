from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)


# class PostListView(ListView):
class PostListView(TemplateView):
    template_name = "blog/post-list.html"


# class PostDetailView(DetailView):
class PostDetailView(TemplateView):
    template_name = "blog/post-detail.html"


class PostDeleteView(TemplateView):
    # class PostDeleteView(DeleteView):
    template_name = "blog/post-delete.html"


class PostNewView(TemplateView):
    # class PostNewView(CreateView):
    template_name = "blog/post-new.html"


class PostUpdateView(TemplateView):
    # class PostUpdateView(UpdateView):
    template_name = "blog/post-update.html"
