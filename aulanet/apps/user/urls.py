
from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("login/", views.auth_login, name="login"),
    path("logout/", views.auth_logout, name="logout"),
    path("register/", views.auth_register, name="register"),

    path("profile/", views.user_profile, name="user-profile"),
    path("profile/edit/", views.user_update, name="user-update"),
]
