from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
