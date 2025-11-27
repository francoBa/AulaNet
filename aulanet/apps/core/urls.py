from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contacto/", ContactView.as_view(), name="contact"),
    path("acerca-de/", AboutView.as_view(), name="about"),
    path("404/", NotFoundView.as_view(), name="404"),
    path("500/", ServerErrorView.as_view(), name="500"),
]
