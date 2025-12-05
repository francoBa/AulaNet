from django import forms
from .models import School, SchoolRating

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            "name",
            "school_type",
            "school_level",
            "city",
            "address",
            "description",
            "image",
            "management_type",
            "number",
        ]
        labels = {
            "name": "Nombre del colegio",
            "school_type": "Tipo de colegio",
            "school_level": "Nivel escolar",
            "city": "Ciudad / Localidad",
            "address": "Dirección",
            "description": "Descripción",
            "image": "Foto",
            "management_type": "Tipo de gestión",
            "number": "Número del colegio",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full p-4 border rounded-lg"}),
            "school_type": forms.Select(attrs={"class": "w-full p-4 border rounded-lg"}),
            "school_level": forms.Select(attrs={"class": "w-full p-4 border rounded-lg"}),
            "city": forms.TextInput(attrs={"class": "w-full p-4 border rounded-lg"}),
            "address": forms.TextInput(attrs={"class": "w-full p-4 border rounded-lg"}),
            "description": forms.Textarea(attrs={"class": "w-full p-4 border rounded-lg", "rows": 4}),
            "image": forms.ClearableFileInput(attrs={"class": "w-full"}),
            "management_type": forms.Select(attrs={"class": "w-full p-4 border rounded-lg"}),
            "number": forms.NumberInput(attrs={"class": "w-full p-4 border rounded-lg"}),
        }

class SchoolRatingForm(forms.ModelForm):
    class Meta:
        model = SchoolRating
        fields = ["value"]
        labels = {"value": "Calificación"}
        help_texts = {"value": "Selecciona un puntaje del 1 al 5"}
        widgets = {
            "value": forms.RadioSelect(choices=[(i, "★"*i) for i in range(1,6)])
        }
