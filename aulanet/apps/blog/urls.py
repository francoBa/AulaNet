from django.urls import path
from .views import *

app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/detalle/", PostDetailView.as_view(), name="post-detail"),
    # path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/nuevo/", PostNewView.as_view(), name="post-new"),
    path("post/editar/", PostUpdateView.as_view(), name="post-update"),
    # path("post/<int:pk>/editar/", PostUpdateView.as_view(), name="post-update"),
    path("post/eliminar/", PostDeleteView.as_view(), name="post-delete"),
    # path("post/<int:pk>/eliminar/", PostDeleteView.as_view(), name="post-delete"),
]
