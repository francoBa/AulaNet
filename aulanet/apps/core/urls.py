from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contacto/", ContactView.as_view(), name="contact"),
    path("acerca-de/", AboutView.as_view(), name="about"),
    path("not-found/", Error404View.as_view(), name="404"),
    path("internal-server-error/", Error500View.as_view(), name="500"),
]
