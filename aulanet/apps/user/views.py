from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .forms import *
from .models import User


class AuthLoginView(LoginView):
    template_name = "auth/auth-login.html"
    authentication_form = LoginForm


class AuthRegisterView(CreateView):
    template_name = "auth/auth-register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("user:login")


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "user/user-profile.html"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/user-update.html"
    success_url = reverse_lazy("user:user-profile")

    def get_object(self):
        return self.request.user
