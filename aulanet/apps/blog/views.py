from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


class PostListView(ListView):
    template_name = "blog/post-list.html"


class PostDetailView(DetailView):
    template_name = "blog/post-detail.html"


class PostDeleteView(DeleteView):
    template_name = "blog/post-delete.html"


class PostNewView(CreateView):
    template_name = "blog/post-new.html"


class PostUpdateView(UpdateView):
    template_name = "blog/post-update.html"
