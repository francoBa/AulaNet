from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import *


class AuthLoginView(LoginView):
    template_name = "auth/auth-login.html"
    authentication_form = LoginForm


class AuthRegisterView(CreateView):
    template_name = "auth/auth-register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("user:login")

    def form_valid(self, form):
        valid = super().form_valid(form)
        return valid


class UserProfileView(TemplateView):
    template_name = "user/user-profile.html"


class UserUpdateView(TemplateView):
    template_name = "user/user-update.html"

    def post(self, request, *args, **kwargs):
        return redirect("user:user-profile")
