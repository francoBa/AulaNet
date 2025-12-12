from django.db import transaction
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import View

from .models import Post, PostImage, Comment, Category
from apps.school.models import School
from .forms import *


class ContributorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (  # type: ignore
            self.request.user.groups.filter(name__in=["Contributor", "Admin"]).exists()  # type: ignore
            or self.request.user.is_superuser  # type: ignore
        )


class AuthorOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()  # type: ignore # Puede ser un Post o un Comment
        user = self.request.user  # type: ignore

        if not user.is_authenticated:
            return False

        # Superuser siempre puede todo
        if user.is_superuser:
            return True

        # El autor siempre puede editar/borrar lo suyo
        if obj.author == user:
            return True

        # ADMIN: Debe ser Admin Y del mismo colegio
        if user.groups.filter(name="Admin").exists():
            # POST
            if hasattr(obj, "school"):
                return user.school == obj.school

            # COMENTARIO
            if hasattr(obj, "post"):
                return user.school == obj.post.school

        return False


class SameSchoolRequiredMixin(UserPassesTestMixin):
    """
    Solo permite acceso si el usuario pertenece al mismo colegio que el Post
    o si es Superusuario.
    """

    def test_func(self):
        user = self.request.user  # type: ignore

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        # Obtenemos el Post basado en la URL
        slug = self.kwargs.get("slug")  # type: ignore
        post = get_object_or_404(Post, slug=slug)

        # ¿Tiene colegio el usuario? Y ¿Es el mismo del post?
        if user.school and post.school:
            return user.school == post.school

        return False


# --- VISTAS DE POSTS ---


class PostListView(ListView):
    model = Post
    template_name = "blog/post-list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.select_related("author", "category", "school").order_by(
            "-created_at"
        )

        # --- LÓGICA DE FILTRADO POR CATEGORÍA ---
        categoria_nombre = self.request.GET.get("categoria")
        if categoria_nombre:
            queryset = queryset.filter(category__name=categoria_nombre)

        # --- LÓGICA DE FILTRADO POR COLEGIO ---
        school_slug = self.request.GET.get("school")
        if school_slug:
            queryset = queryset.filter(school__slug=school_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # menú de filtros
        context["categories"] = Category.objects.all()
        school_slug = self.request.GET.get("school")
        if school_slug:
            context["current_school"] = get_object_or_404(School, slug=school_slug)

        context["selected_category"] = self.request.GET.get("categoria")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post-detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.select_related("author").order_by(  # type: ignore
            "-created_at"
        )
        return context


class PostCreateView(LoginRequiredMixin, ContributorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post-form.html"

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.request.user.school:  # type: ignore
            form.instance.school = self.request.user.school  # type: ignore

        self.object = form.save()

        # --- LÓGICA DE IMÁGENES ---
        images = self.request.FILES.getlist("extra_images")

        if images:
            for image in images:
                PostImage.objects.create(post=self.object, image=image)
        else:
            default_img = getattr(
                settings, "POST_DEFAULT_IMAGE", "posts/default/post-default.jpg"
            )
            PostImage.objects.create(post=self.object, image=default_img)

        messages.success(self.request, "Post creado exitosamente.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, AuthorOrAdminMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post-form.html"

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.object.slug})  # type: ignore


class PostDeleteView(LoginRequiredMixin, AuthorOrAdminMixin, DeleteView):
    model = Post
    template_name = "blog/post-delete.html"
    success_url = reverse_lazy("blog:post-list")


# --- VISTAS DE COMENTARIOS  ---


class CommentCreateView(LoginRequiredMixin, SameSchoolRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment-form.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs["slug"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.kwargs["slug"]})


class CommentUpdateView(LoginRequiredMixin, AuthorOrAdminMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment-form.html"

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.object.post.slug})  # type: ignore


class CommentDeleteView(LoginRequiredMixin, AuthorOrAdminMixin, DeleteView):
    model = Comment
    template_name = "blog/comment-delete.html"

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.object.post.slug})  # type: ignore
