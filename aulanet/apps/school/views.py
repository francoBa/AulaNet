from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView
from .models import School, Review, SchoolRating
from .forms import SchoolForm
from django.urls import reverse, reverse_lazy
from apps.blog.models import Post


# 1) Create (solo plantilla por ahora)
class CreateSchoolView(CreateView):
    model = School
    form_class = SchoolForm
    template_name = "school/create-school.html"
    success_url = reverse_lazy("school:school-list")


# 2) Listado real (CLASE) con filtros
class ListSchoolView(View):
    template_name = "school/school-list.html"

    def get(self, request):
        search = request.GET.get("search", "")
        tipo = request.GET.get("tipo", "")

        schools = School.objects.all()

        # Filtro por buscador
        if search:
            schools = schools.filter(name__icontains=search) | schools.filter(
                city__icontains=search
            )

        # Filtro por tipo
        if tipo:
            schools = schools.filter(school_type=tipo)

        context = {
            "schools": schools,
            "search": search,
            "tipo": tipo,
        }
        return render(request, self.template_name, context)


# ReviewSchoolView eliminado o simplificado si no hay ratings
# solo para mostrar las escuelas
class ReviewSchoolView(View):
    def get(self, request):
        schools = School.objects.all()
        return render(request, "school/review-school.html", {"schools": schools})

    def post(self, request):
        # Si no vas a manejar ratings, por ahora solo redirige
        return render(
            request, "school/review-school.html", {"schools": School.objects.all()}
        )


# Detalle de la escuela sin ratings
class SchoolDetailView(DetailView):
    model = School
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "school/school-detail.html"
    context_object_name = "school"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        school = self.get_object()
        # los últimos 4 posts de ESTE colegio
        latest_posts = Post.objects.filter(school=school).order_by("-created_at")[:4]

        # Añadimos los posts al contexto
        context["latest_posts"] = latest_posts

        return context

    def post(self, request, pk):
        # Sin ratings, solo redirigir al detalle
        return redirect("school:school-detail", pk=pk)
