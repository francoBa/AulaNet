from django.urls import path
from .views import (
    CreateSchoolView,
    ListSchoolView,
    SchoolDetailView,
    ReviewSchoolView,
    RateSchoolView
)

app_name = "school"

urlpatterns = [
    path("crear/", CreateSchoolView.as_view(), name="create-school"),
    path("", ListSchoolView.as_view(), name="school-list"),
    path("<slug:slug>/", SchoolDetailView.as_view(), name="school-detail"),
    path("<slug:slug>/reseñas/", ReviewSchoolView.as_view(), name="review-school"),
    path("<slug:slug>/puntuar/", RateSchoolView.as_view(), name="rate-school"),
]
