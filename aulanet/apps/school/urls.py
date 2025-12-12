from django.urls import path
from .views import *

app_name = "school"

urlpatterns = [
    path("escuela/crear/", CreateSchoolView.as_view(), name="create-school"),
    path("escuela/listar/", ListSchoolView.as_view(), name="school-list"),
    path("escuela/calificar/", ReviewSchoolView.as_view(), name="review-school"),
    path("escuela/<slug:slug>/", SchoolDetailView.as_view(), name="school-detail"),
]
