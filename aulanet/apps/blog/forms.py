from django import forms
from .models import Post, Comment


# --- WIDGET PERSONALIZADO PARA MÚLTIPLES ARCHIVOS ---
class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class TailwindMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # type: ignore
            if not isinstance(field.widget, (forms.FileInput, forms.CheckboxInput)):
                clases = (
                    "w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-slate-600 "
                    "bg-white dark:bg-slate-700 text-gray-900 dark:text-white "
                    "focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200"
                )
                field.widget.attrs["class"] = clases


class PostForm(TailwindMixin, forms.ModelForm):
    # Campo extra para manejar múltiples imágenes
    extra_images = forms.FileField(
        label="Imágenes de Galería (Opcional)",
        required=False,
        widget=MultipleFileInput(
            attrs={
                "multiple": True,
                "class": "js-file-input hidden",
            }
        ),
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "content",
            "image",
            "extra_images",
            "allow_comments",
        ]

        labels = {
            "title": "Título del Artículo",
            "category": "Categoría",
            "content": "Contenido",
            "image": "Imagen de Portada",
            "allow_comments": "Permitir comentarios",
        }

        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Escribe el contenido aquí..."}
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "js-file-input hidden",
                }
            ),
            "allow_comments": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 h-5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600 cursor-pointer"
                }
            ),
        }


class CommentForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": "Deja tu comentario"}
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Escribe un comentario respetuoso..."}
            ),
        }
