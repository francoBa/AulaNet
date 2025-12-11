from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import FileInput
from .models import User

INPUT_CLASSES = (
    "w-full px-4 py-3 rounded-lg border "
    "border-gray-300 dark:border-slate-600 "
    "bg-gray-50 dark:bg-slate-700 "
    "text-gray-900 dark:text-white "
    "placeholder-gray-400 dark:placeholder-gray-400 "
    "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent "
    "transition duration-200 ease-in-out"
)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": INPUT_CLASSES,
                "placeholder": "Usuario o Email",
                "autofocus": True,
            }
        )
        self.fields["password"].widget.attrs.update(
            {"class": INPUT_CLASSES, "placeholder": "Contraseña"}
        )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "school")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": INPUT_CLASSES})

        self.fields["school"].required = True

        placeholders = {
            "username": "Ej: juanperez",
            "email": "juan@ejemplo.com",
            "first_name": "Juan",
            "last_name": "Pérez",
            "password1": "Mínimo 8 caracteres",
            "password2": "Repite la contraseña",
        }

        for name, text in placeholders.items():
            self.fields[name].widget.attrs["placeholder"] = text

        self.fields["username"].widget.attrs["autofocus"] = True


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "city",
            "birthdate",
            "school",
            "related_school",
            "avatar",
        ]
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "related_school": "Relación con el colegio",
            "birthdate": "Fecha de Nacimiento",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES

        self.fields["birthdate"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": INPUT_CLASSES}
        )

        self.fields["avatar"].widget = FileInput(
            attrs={"class": "hidden js-file-input", "id": "id_avatar"}
        )
