from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .models import School


# 1) Create (solo plantilla por ahora)
class CreateSchoolView(TemplateView):
    template_name = "school/create-school.html"


# 2) Listado real (CLASE) con filtros
class ListSchoolView(View):
    template_name = "school/school-list.html"

    def get(self, request):
        search = request.GET.get("search", "")
        tipo = request.GET.get("tipo", "")

        schools = School.objects.all()

        # Filtro por buscador
        if search:
            schools = schools.filter(name__icontains=search) | schools.filter(city__icontains=search)

        # Filtro por tipo
        if tipo:
            schools = schools.filter(school_type=tipo)

        context = {
            "schools": schools,
            "search": search,
            "tipo": tipo,
        }
        return render(request, self.template_name, context)


#ReviewSchoolView eliminado o simplificado si no hay ratings
# solo para mostrar las escuelas
class ReviewSchoolView(View):
    def get(self, request):
        schools = School.objects.all()
        return render(request, "school/review-school.html", {"schools": schools})

    def post(self, request):
        # Si no vas a manejar ratings, por ahora solo redirige
        return render(request, "school/review-school.html", {"schools": School.objects.all()})


# Detalle de la escuela sin ratings
class SchoolDetailView(View):
    def get(self, request, pk):
        school = get_object_or_404(School, pk=pk)
        return render(request, "school/school-detail.html", {
            "school": school
        })

    def post(self, request, pk):
        # Sin ratings, solo redirigir al detalle
        return redirect("school:school-detail", pk=pk)
