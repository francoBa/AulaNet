from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    CommentAddView,
    CommentEditView,
    CommentDeleteView,
    school_rating_view,
)

app_name = "blog"

urlpatterns = [
    # Lista de posts (PÚBLICA)
    path("posts/", PostListView.as_view(), name="post-list"),
    
    # Detalle de post (PÚBLICO)
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    
    # Comentarios (PRIVADO)
    path("comment/add/<slug:slug>/", CommentAddView.as_view(), name="comment-add"),
    path("comment/edit/<int:pk>/", CommentEditView.as_view(), name="comment-edit"),
    path("comment/delete/<int:pk>/", CommentDeleteView.as_view(), name="comment-delete"),
    
    # Puntuación de la escuela (PRIVADO)
    path("school/<int:school_id>/rate/", school_rating_view, name="school-rate"),
    path("school/<int:school_id>/rate/<slug:post_slug>/", school_rating_view, name="school-rate-post"),
]
