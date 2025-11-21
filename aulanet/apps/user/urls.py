from django.urls import path
from .views import *

app_name = "user"


urlpatterns = [
    path("user/profile", UserProfileView.as_view(), name="user-profile"),
    # path("user/profile/<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path("user/profile/edit/", UserUpdateView.as_view(), name="user-update"),
    # path("user/profile/<int:pk>/edit/", UserUpdateView.as_view(), name="user-update"),
]
