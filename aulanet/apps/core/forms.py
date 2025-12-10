from django import forms

class ContactForm(forms.Form):

    name = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre completo",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-md border border-gray-300 dark:border-slate-600 "
                     "bg-gray-50 dark:bg-slate-700 text-text focus:ring-2 focus:ring-color-secondary "
                     "transition",
            "placeholder": "Tu nombre",
            "autocomplete": "name"
        })
    )

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 rounded-md border border-gray-300 dark:border-slate-600 "
                     "bg-gray-50 dark:bg-slate-700 text-text focus:ring-2 focus:ring-color-secondary "
                     "transition",
            "placeholder": "tuemail@ejemplo.com",
            "autocomplete": "email"
        })
    )

    subject = forms.CharField(
        max_length=200,
        required=True,
        label="Asunto",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-md border border-gray-300 dark:border-slate-600 "
                     "bg-gray-50 dark:bg-slate-700 text-text focus:ring-2 focus:ring-color-secondary "
                     "transition",
            "placeholder": "Motivo del contacto"
        })
    )

    message = forms.CharField(
        required=True,
        label="Mensaje",
        widget=forms.Textarea(attrs={
            "rows": 5,
            "class": "w-full px-4 py-3 rounded-md border border-gray-300 dark:border-slate-600 "
                     "bg-gray-50 dark:bg-slate-700 text-text focus:ring-2 focus:ring-color-secondary "
                     "transition",
            "placeholder": "Escribí tu mensaje"
        })
    )
