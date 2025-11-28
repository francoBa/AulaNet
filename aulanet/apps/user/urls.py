from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    # AUTH SYSTEM
    path("login/", AuthLoginView.as_view(), name="login"),
    path("register/", AuthRegisterView.as_view(), name="register"),

    # USER PROFILE
    path("user/profile/", UserProfileView.as_view(), name="user-profile"),
    path("user/profile/edit/", UserUpdateView.as_view(), name="user-update"),
]
