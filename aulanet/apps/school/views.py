from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    ListView,
    DeleteView,
)
from .models import School, Review, SchoolRating
from .forms import *
from django.urls import reverse, reverse_lazy
from apps.blog.models import Post
from apps.user.models import User


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



class SchoolRatingView(View):
    def get(self, request, slug):
        school = get_object_or_404(School, slug=slug)

        if request.user.school != school:
            return HttpResponseForbidden()

        if SchoolRating.objects.filter(school=school, user=request.user).exists():
            return redirect("school:school-detail", slug=slug)

        form = SchoolRatingForm()

        return render(request, "school/review-school.html", {
            "school": school,
            "form": form,
        })

    def post(self, request, slug):
        school = get_object_or_404(School, slug=slug)
        user = request.user

        if user.school != school:
            return HttpResponseForbidden()

        if SchoolRating.objects.filter(school=school, user=user).exists():
            return redirect("school:school-detail", slug=slug)

        form = SchoolRatingForm(request.POST)

        if not form.is_valid():
            return render(request, "school/review-school.html", {
                "school": school,
                "form": form,
            })

        # ---- agrupar datos por área ----
        pedagogica = {k: int(form.cleaned_data[k]) for k in PEDAGOGICA_FIELDS}
        cultura = {k: int(form.cleaned_data[k]) for k in CULTURA_FIELDS}
        bienestar = {k: int(form.cleaned_data[k]) for k in BIENESTAR_FIELDS}
        recursos = {k: int(form.cleaned_data[k]) for k in RECURSOS_FIELDS}

        all_scores = (
            list(pedagogica.values())
            + list(cultura.values())
            + list(bienestar.values())
            + list(recursos.values())
        )

        average = round(sum(all_scores) / len(all_scores), 2)

        SchoolRating.objects.create(
            school=school,
            user=user,
            pedagogica=pedagogica,
            cultura=cultura,
            bienestar=bienestar,
            recursos=recursos,
            average_score=average,
        )

        school.update_rating()

        return redirect("school:school-detail", slug=slug)

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
        user = self.request.user
        if user.is_authenticated:
            context["user_rating"] = SchoolRating.objects.filter(
                school=school, user=user
            ).first()
        else:
            context["user_rating"] = None

        return context
        # los últimos 4 posts de ESTE colegio
        latest_posts = Post.objects.filter(school=school).order_by("-created_at")[:4]

        # Añadimos los posts al contexto
        context["latest_posts"] = latest_posts

        return context

    def post(self, request, pk):
        # Sin ratings, solo redirigir al detalle
        return redirect("school:school-detail", pk=pk)
    
    


# --- administración de usuarios del colegio (Admin role) -----


# --- MIXIN DE PERMISOS ---
class AdminRequiredMixin(UserPassesTestMixin):
    """
    Verifica que el usuario esté logueado y pertenezca al grupo 'Admin'.
    """

    def test_func(self):
        return self.request.user.is_authenticated and (  # type: ignore
            self.request.user.groups.filter(name="Admin").exists()  # type: ignore
            or self.request.user.is_superuser  # type: ignore
        )


# --- LISTAR USUARIOS DEL COLEGIO ---
class SchoolUserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = "school/admin/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        """
        Esta es la clave: Filtra los usuarios para mostrar solo los
        del mismo colegio que el admin logueado.
        También se excluye a sí mismo de la lista.
        """
        queryset = super().get_queryset()
        return (
            queryset.filter(school=self.request.user.school)  # type: ignore
            .exclude(pk=self.request.user.pk)
            .prefetch_related("groups")
        )

    def get_context_data(self, **kwargs):
        """
        Añade los roles disponibles al contexto para rellenar el
        menú desplegable en la plantilla.
        """
        context = super().get_context_data(**kwargs)
        # Un Admin de colegio solo puede asignar roles inferiores, nunca 'Admin'.
        context["available_groups"] = Group.objects.filter(
            name__in=["Registered", "Contributor"]
        )
        return context


# --- PROCESAR EL CAMBIO DE ROL ---
class UserRoleUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        # Obtener el usuario que se va a modificar
        target_user = get_object_or_404(User, pk=pk)

        # Asegurarse de que el admin no modifique usuarios de otros colegios
        if target_user.school != request.user.school or target_user.is_superuser:
            return HttpResponseForbidden(
                "No tienes permiso para modificar a este usuario."
            )

        new_group_id = request.POST.get("group")
        if not new_group_id:
            messages.error(request, "No se seleccionó un nuevo rol.")
            return redirect("school:school-user-list")

        new_group = get_object_or_404(Group, pk=new_group_id)

        # no permitir promover a Admin
        if new_group.name not in ["Registered", "Contributor"]:
            return HttpResponseForbidden("No se puede asignar este rol.")

        # Asignar el nuevo rol (eliminando los anteriores)
        target_user.groups.clear()
        target_user.groups.add(new_group)

        messages.success(
            request,
            f"Se actualizó el rol de {target_user.username} a {new_group.name}.",
        )
        return redirect("school:school-user-list")


# --- 4. VISTA PARA ELIMINAR UN USUARIO ---
class SchoolUserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = "school/admin/user_delete_confirm.html"
    success_url = reverse_lazy("school:school-user-list")
    context_object_name = "user_to_delete"

    def get_queryset(self):
        """
        Asegura que un admin solo pueda ver la página de confirmación
        para usuarios de su propio colegio.
        """
        queryset = super().get_queryset()
        return queryset.filter(school=self.request.user.school)  # type: ignore

    def form_valid(self, form):
        messages.success(
            self.request, f"El usuario {self.object.username} ha sido eliminado."  # type: ignore
        )
        return super().form_valid(form)  # type: ignore
