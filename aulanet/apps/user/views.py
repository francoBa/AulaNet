from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# Authentication (render-only for now)
class AuthLoginView(TemplateView):
    template_name = "auth/auth-login.html"

class AuthRegisterView(TemplateView):
    template_name = "auth/auth-register.html"

# User profile
class UserProfileView(TemplateView):
    template_name = "user/user-profile.html"
from django.views.generic import FormView, TemplateView
from django import forms

# Temporary forms (so FormView doesn't crash)
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class AuthLoginView(FormView):
    template_name = "auth/auth-login.html"
    form_class = LoginForm
    success_url = "/"


class AuthRegisterView(FormView):
    template_name = "auth/auth-register.html"
    form_class = RegisterForm
    success_url = "/login/"


class UserProfileView(TemplateView):
    template_name = "user/user-profile.html"


class UserUpdateView(TemplateView):
    template_name = "user/user-update.html"

    def post(self, request, *args, **kwargs):
        # Aquí iría la lógica para actualizar los datos del usuario
        # Por ahora, solo redirigimos al perfil del usuario
        return redirect("user:user-profile")