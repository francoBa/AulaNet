from django.urls import path
from .views import *

app_name = "school"

urlpatterns = [
    path("escuela/crear/", CreateSchoolView.as_view(), name="create-school"),
    path("escuela/listar/", school_list, name="school-list"),       # nombre namespaced: school:school-list
    path("escuela/calificar/", ReviewSchoolView.as_view(), name="review-school"),
    path("escuela/<int:pk>/", SchoolDetailView.as_view(), name="school-detail"),
]
