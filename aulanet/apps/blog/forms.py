# forms.py
from django import forms
from .models import Post, PostImage, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "categoria", "contenido"]

        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white placeholder-gray-400",
                "placeholder": "Ej: Ganadores de la feria de ciencias" + "appearance-none",
            }),
            "categoria": forms.Select(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white" +"appearance-none",
            }),
            "contenido": forms.Textarea(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 resize-none bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white placeholder-gray-400"+ "resize-none",
                "rows": 6,
                "placeholder": "Escribe aquí el detalle de tu publicación..."
            }),
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ["imagen"]
        widgets = {
            "imagen": forms.ClearableFileInput(attrs={
                "multiple": True,
                "class": "hidden",
                "id": "imagenes",
            })
        }
