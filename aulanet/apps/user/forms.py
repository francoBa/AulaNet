from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "city", "related_school", "type", "birthdate"]

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    score = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=5,
        label="Puntuación de tu escuela",
        help_text="Solo puedes tener una puntuación. Puedes modificarla aquí."
    )

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email", "city",
            "related_school", "type", "birthdate",
            "avatar", "school", "score"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input-field"}),
            "last_name": forms.TextInput(attrs={"class": "input-field"}),
            "email": forms.EmailInput(attrs={"class": "input-field"}),
            "city": forms.TextInput(attrs={"class": "input-field"}),
            "related_school": forms.TextInput(attrs={"class": "input-field"}),
            "type": forms.TextInput(attrs={"class": "input-field"}),
            "birthdate": forms.DateInput(attrs={"type": "date", "class": "input-field"}),
            "school": forms.Select(attrs={"class": "input-field"}),
            "score": forms.NumberInput(attrs={"class": "input-field", "min": 1, "max": 5}),
            "avatar": forms.ClearableFileInput(attrs={"class": "input-field"}),
        }

class LoginForm(forms.Form):
    email_or_username = forms.CharField(label="Usuario o email")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        email_or_username = cleaned_data.get("email_or_username")
        password = cleaned_data.get("password")
        user = None

        if email_or_username and password:
            # Intentar buscar usuario por email
            try:
                user_obj = User.objects.get(email=email_or_username)
                username = user_obj.username
            except User.DoesNotExist:
                username = email_or_username

            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")

        cleaned_data["user"] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get("user")
