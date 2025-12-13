from django.urls import path
from .views import *

app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/nuevo/", PostCreateView.as_view(), name="post-create"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<slug:slug>/editar/", PostUpdateView.as_view(), name="post-update"),
    path("post/<slug:slug>/eliminar/", PostDeleteView.as_view(), name="post-delete"),
    # Comentarios
    path(
        "post/<slug:slug>/comentarios/nuevo/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comentarios/<uuid:pk>/editar/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comentarios/<uuid:pk>/eliminar/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
