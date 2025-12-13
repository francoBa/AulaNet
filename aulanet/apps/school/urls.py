from django.urls import path
from .views import *

app_name = "school"

urlpatterns = [
    path("escuela/crear/", CreateSchoolView.as_view(), name="create-school"),
    path("escuela/listar/", ListSchoolView.as_view(), name="school-list"),
    path("escuela/<slug:slug>/calificar/", SchoolRatingView.as_view(), name="review-school"),
    path("escuela/<slug:slug>/", SchoolDetailView.as_view(), name="school-detail"),
    # --- URLS DE GESTIÓN DE USUARIOS DEL COLEGIO ---
    path("mi-colegio/usuarios/", SchoolUserListView.as_view(), name="school-user-list"),
    path(
        "mi-colegio/usuarios/<uuid:pk>/actualizar-rol/",
        UserRoleUpdateView.as_view(),
        name="school-user-role-update",
    ),
    path(
        "mi-colegio/usuarios/<uuid:pk>/eliminar/",
        SchoolUserDeleteView.as_view(),
        name="school-user-delete",
    ),
]
