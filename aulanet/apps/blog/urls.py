

from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    CommentAddView,
    CommentEditView,
    CommentDeleteView,
    school_rating_view,
    PostCreateView,
    PostEditView,
    PostDeleteView,
)

app_name = "blog"

urlpatterns = [
    # Lista de posts (PÚBLICA)
    path("posts/", PostListView.as_view(), name="post-list"),

    # Crear post asociado a una escuela (PRIVADO)
    path("school/<slug:school_slug>/post/new/", PostCreateView.as_view(), name="post-new"),

    # Detalle de post (PÚBLICO)
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    
    # Editar post (solo autor)
    path("post/<slug:slug>/edit/", PostEditView.as_view(), name="post-edit"),

# Eliminar post (solo autor)
    path("post/<slug:slug>/delete/", PostDeleteView.as_view(), name="post-delete"),


    # Comentarios (PRIVADO)
    path("comment/add/<slug:slug>/", CommentAddView.as_view(), name="comment-add"),
    path("comment/edit/<uuid:pk>/", CommentEditView.as_view(), name="comment-edit"),
    path("comment/delete/<uuid:pk>/", CommentDeleteView.as_view(), name="comment-delete"),


    # Puntuación de escuela (PRIVADO) - USANDO slug
    path("school/<slug:school_slug>/rate/", school_rating_view, name="school-rate"),
    path("school/<slug:school_slug>/rate/<slug:post_slug>/", school_rating_view, name="school-rate-post"),
]
