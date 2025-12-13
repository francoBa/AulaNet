from django import forms
from .models import School, Review, SchoolRating

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["name", "school_type", "school_level", "city", "address", "description", "image"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white placeholder-gray-400" + "appearance-none",
                "placeholder": "Ej: Escuela Primaria N° 1234" ,
            }),
            "school_type": forms.Select(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white" +"appearance-none",
            }),
            "school_level": forms.Select(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white" +"appearance-none",
            }),
            "city": forms.TextInput(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white placeholder-gray-400" + "appearance-none",
                "placeholder": "Ej: Buenos Aires",
            }),
            "address": forms.TextInput(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white placeholder-gray-400" + "appearance-none",
                "placeholder": "Ej: Av. Siempre Viva 742",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 resize-none bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white placeholder-gray-400"+ "resize-none" + "appearance-none",
                "placeholder": "Descripción de la escuela",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "w-full p-4 border border-gray-500 dark:border-slate-600 rounded-lg shadow-sm "
                         "focus:border-blue-500 focus:ring-blue-500 bg-white dark:bg-slate-700 "
                         "text-gray-900 dark:text-white" +"appearance-none",
            }),
        }

RATING_CHOICES = [
    (1, "Muy malo"),
    (2, "Malo"),
    (3, "Regular"),
    (4, "Bueno"),
    (5, "Muy bueno"),
]

PEDAGOGICA_FIELDS = ["docentes", "metodologia", "contenidos"]
CULTURA_FIELDS = ["convivencia", "inclusion"]
BIENESTAR_FIELDS = ["acompanamiento", "orientacion"]
RECURSOS_FIELDS = ["infraestructura", "tecnologia"]


class SchoolRatingForm(forms.ModelForm):
    docentes = forms.ChoiceField(
        label="Calidad de los docentes",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    metodologia = forms.ChoiceField(
        label="Metodología de enseñanza",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    contenidos = forms.ChoiceField(
        label="Contenidos educativos",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    convivencia = forms.ChoiceField(
        label="Convivencia escolar",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    inclusion = forms.ChoiceField(
        label="Inclusión",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    acompanamiento = forms.ChoiceField(
        label="Acompañamiento al alumno",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    orientacion = forms.ChoiceField(
        label="Orientación escolar",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    infraestructura = forms.ChoiceField(
        label="Infraestructura",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    tecnologia = forms.ChoiceField(
        label="Tecnología y recursos digitales",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = SchoolRating
        fields = []

