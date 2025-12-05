from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import School, Review, SchoolRating
from .forms import SchoolForm


class CreateSchoolView(View):
    template_name = "school/create-school.html"

    def get(self, request):
        form = SchoolForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            school = form.save()
            messages.success(request, f"La escuela '{school.name}' se creó correctamente.")
            return redirect("school:school-detail", slug=school.slug)

        messages.error(request, "Hubo errores en el formulario. Por favor revisa los datos.")
        return render(request, self.template_name, {"form": form})


class ListSchoolView(View):
    template_name = "school/school-list.html"

    def get(self, request):
        search = request.GET.get("search", "")
        tipo = request.GET.get("tipo", "")

        schools = School.objects.all()

        if search:
            schools = schools.filter(
                models.Q(name__icontains=search) |
                models.Q(city__icontains=search)
            )

        if tipo:
            schools = schools.filter(school_type=tipo)

        # Calcular promedio de estrellas
        for school in schools:
            ratings = school.ratings.all()
            school.average_rating = (
                sum(r.value for r in ratings) / ratings.count()
                if ratings.exists() else 0
            )

        return render(request, self.template_name,
            {"schools": schools, "search": search, "tipo": tipo}
        )


class SchoolDetailView(View):
    template_name = "school/school-detail.html"

    def get(self, request, slug):
        school = get_object_or_404(School, slug=slug)

        ratings = school.ratings.all()
        average = (
            sum(r.value for r in ratings) / ratings.count()
            if ratings.exists() else 0
        )

        return render(request, self.template_name, {
            "school": school,
            "ratings": ratings,
            "average": round(average, 1)
        })


@method_decorator(login_required, name='dispatch')
class RateSchoolView(View):

    def post(self, request, slug):
        school = get_object_or_404(School, slug=slug)
        value = int(request.POST.get("value", 0))

        if value < 1 or value > 5:
            messages.error(request, "Valor inválido.")
            return redirect("school:school-detail", slug=slug)

        # Si el usuario ya calificó → actualiza
        rating, created = SchoolRating.objects.update_or_create(
            user=request.user,
            school=school,
            defaults={"value": value}
        )

        if created:
            messages.success(request, "¡Gracias por puntuar!")
        else:
            messages.success(request, "Tu calificación fue actualizada.")

        return redirect("school:school-detail", slug=slug)


@method_decorator(login_required, name='dispatch')
class ReviewSchoolView(View):
    template_name = "school/review-school.html"

    def get(self, request, slug):
        school = get_object_or_404(School, slug=slug)
        return render(request, self.template_name, {"school": school})

    def post(self, request, slug):
        school = get_object_or_404(School, slug=slug)
        comment = request.POST.get("comment")

        if not comment:
            messages.error(request, "El comentario no puede estar vacío.")
            return redirect("school:review-school", slug=slug)

        Review.objects.create(
            school=school,
            author=request.user,
            comment=comment
        )

        messages.success(request, "Tu reseña fue publicada.")
        return redirect("school:review-school", slug=slug)
