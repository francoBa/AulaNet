from django import forms
from .models import Comment, Post, Category

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "category", "content", "image"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded-lg dark:bg-gray-800 dark:text-white"
            }),
            "category": forms.Select(attrs={
                "class": "w-full p-2 border rounded-lg dark:bg-gray-800 dark:text-white"
            }),
            "content": forms.Textarea(attrs={
                "rows": 6,
                "class": "w-full p-2 border rounded-lg dark:bg-gray-800 dark:text-white"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "w-full p-2 border rounded-lg dark:bg-gray-800 dark:text-white"
            }),
        }

    # ⭐ ESTA ES LA PARTE QUE FALTABA ⭐
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
