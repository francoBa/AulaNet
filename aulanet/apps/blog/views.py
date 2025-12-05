from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q

from .models import Post, Comment, Category
from .forms import CommentForm
from apps.school.models import School, SchoolRating
from apps.school.forms import SchoolRatingForm

# ==========================
# LISTA Y DETALLE DE POSTS (PÚBLICOS)
# ==========================

class PostListView(ListView):  # ← SIN LoginRequired
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
            queryset = queryset.filter(author__school_id=school_id)
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


class PostDetailView(DetailView):  # ← SIN LoginRequired
    model = Post
    template_name = "blog/post-detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = post.comment_set.all().order_by("-created_at")
        context["comment_form"] = CommentForm()
        return context

# ==========================
# COMENTARIOS (PRIVADOS)
# ==========================

@method_decorator(login_required, name="dispatch")
class CommentAddView(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.user.school != post.author.school:
            messages.error(request, "Solo puedes comentar posts de tu escuela.")
            return redirect("blog:post-detail", slug=slug)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comentario agregado correctamente.")
        else:
            messages.error(request, "Hubo un error al agregar el comentario.")
        return redirect("blog:post-detail", slug=slug)


@method_decorator(login_required, name="dispatch")
class CommentEditView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        if not (request.user.is_staff or comment.user == request.user):
            messages.error(request, "No tienes permiso para editar este comentario.")
            return redirect("blog:post-detail", slug=comment.post.slug)

        form = CommentForm(instance=comment)
        return render(request, "blog/comment-edit.html", {"form": form})

    def post(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        if not (request.user.is_staff or comment.user == request.user):
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
        if not (request.user.is_staff or comment.user == request.user):
            messages.error(request, "No tienes permiso para eliminar este comentario.")
            return redirect("blog:post-detail", slug=comment.post.slug)

        comment.delete()
        messages.success(request, "Comentario eliminado correctamente.")
        return redirect("blog:post-detail", slug=comment.post.slug)


# ==========================
# PUNTUACIÓN DE ESCUELA (PRIVADO)
# ==========================

@login_required
def school_rating_view(request, school_id, post_slug=None):
    school = get_object_or_404(School, id=school_id)

    try:
        rating_instance = SchoolRating.objects.get(school=school, user=request.user)
    except SchoolRating.DoesNotExist:
        rating_instance = None

    if request.method == "POST":
        form = SchoolRatingForm(request.POST, instance=rating_instance)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.school = school
            rating.user = request.user
            rating.save()
            messages.success(request, "Puntuación registrada correctamente.")
            if post_slug:
                return redirect("blog:post-detail", slug=post_slug)
            return redirect("blog:post-list")
        else:
            messages.error(request, "Hubo un error al guardar la puntuación.")
    else:
        form = SchoolRatingForm(instance=rating_instance)

    return render(
        request,
        "school/review-school.html",
        {"form": form, "school": school, "post_slug": post_slug},
    )
