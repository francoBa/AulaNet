# C:\Users\the_s\OneDrive\Escritorio\Escuela\AulaNet\aulanet\apps\blog\views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment, Category
from .forms import CommentForm, PostForm
from apps.school.models import School, SchoolRating
from apps.school.forms import SchoolRatingForm


# ==========================
# CREAR POST (PRIVADO)
# ==========================
@method_decorator(login_required, name="dispatch")
class PostCreateView(View):
    def get(self, request, school_slug):
        school = get_object_or_404(School, slug=school_slug)
        form = PostForm()
        return render(request, "blog/post-new.html", {"form": form, "school": school})

    def post(self, request, school_slug):
        school = get_object_or_404(School, slug=school_slug)
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.school = school
            post.save()

            messages.success(request, "Tu post fue creado correctamente.")
            return redirect("blog:post-detail", slug=post.slug)

        return render(request, "blog/post-new.html", {"form": form, "school": school})


# ==========================
# LISTA Y DETALLE DE POSTS (PÚBLICOS)
# ==========================
class PostListView(ListView):
    model = Post
    template_name = "blog/post-list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-created_at")

        q = self.request.GET.get("q")
        school_id = self.request.GET.get("school")
        category_id = self.request.GET.get("category")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(content__icontains=q))

        if school_id:
            queryset = queryset.filter(school_id=school_id)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)

        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schools"] = School.objects.all()
        context["categories"] = Category.objects.all()

        context["q"] = self.request.GET.get("q", "")
        context["selected_school"] = self.request.GET.get("school", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["date_from"] = self.request.GET.get("date_from", "")
        context["date_to"] = self.request.GET.get("date_to", "")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post-detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = post.comments.all().order_by("-created_at")
        context["comment_form"] = CommentForm()
        return context


# ==========================
# EDITAR POST (PRIVADO)
# ==========================
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post-update.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "El post fue actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.object.slug})



# ==========================
# ELIMINAR POST (PRIVADO)
# ==========================
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post-delete.html"  
    context_object_name = "post"

    # SOLO permite eliminar al autor
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    # A dónde redirige DESPUÉS de borrar
    def get_success_url(self):
        messages.success(self.request, "El post fue eliminado correctamente.")
        return reverse("blog:post-list")



# ==========================
# COMENTARIOS
# ==========================
@method_decorator(login_required, name="dispatch")
class CommentAddView(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if request.user.school != post.school:
            messages.error(request, "Solo puedes comentar posts de tu escuela.")
            return redirect("blog:post-detail", slug=slug)

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            messages.success(request, "Comentario agregado correctamente.")
        else:
            messages.error(request, "Hubo un error al agregar el comentario.")

        return redirect("blog:post-detail", slug=slug)


@method_decorator(login_required, name="dispatch")
class CommentEditView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if not (request.user.is_staff or comment.author == request.user):
            messages.error(request, "No tienes permiso para editar este comentario.")
            return redirect("blog:post-detail", slug=comment.post.slug)

        form = CommentForm(instance=comment)
        return render(request, "blog/comment-edit.html", {"form": form})

    def post(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if not (request.user.is_staff or comment.author == request.user):
            messages.error(request, "No tienes permiso para editar este comentario.")
            return redirect("blog:post-detail", slug=comment.post.slug)

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            messages.success(request, "Comentario actualizado correctamente.")
            return redirect("blog:post-detail", slug=comment.post.slug)

        return render(request, "blog/comment-edit.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class CommentDeleteView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        if not (request.user.is_staff or comment.author == request.user):
            messages.error(request, "No tienes permiso para eliminar este comentario.")
            return redirect("blog:post-detail", slug=comment.post.slug)

        comment.delete()
        messages.success(request, "Comentario eliminado correctamente.")
        return redirect("blog:post-detail", slug=comment.post.slug)


# ==========================
# PUNTUACIÓN DE ESCUELAS
# ==========================
@login_required
def school_rating_view(request, school_slug, post_slug=None):
    school = get_object_or_404(School, slug=school_slug)

    post = get_object_or_404(Post, slug=post_slug, school=school) if post_slug else None

    if request.method == "POST":
        form = SchoolRatingForm(request.POST)

        if form.is_valid():
            SchoolRating.objects.update_or_create(
                user=request.user,
                school=school,
                post=post,
                defaults={"rating": form.cleaned_data["rating"]},
            )
            messages.success(request, "¡Tu puntuación fue registrada correctamente!")
            return redirect("blog:post-detail", slug=post.slug if post else "")
    else:
        form = SchoolRatingForm()

    return render(
        request,
        "blog/school-rate.html",
        {"form": form, "school": school, "post": post},
    )
