# apps/blog/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Ajusta según tu modelo Comment
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
