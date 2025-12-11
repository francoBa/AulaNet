from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .forms import *
from .models import User


class AuthLoginView(LoginView):
    template_name = "auth/auth-login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
            return next_url
        return self.request.META.get("HTTP_REFERER") or reverse_lazy("core:index")

class AuthRegisterView(CreateView):
    template_name = "auth/auth-register.html"
    form_class = RegisterForm
    
    def form_valid(self, form):
        user = form.save()

        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
            return redirect(next_url)

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("user:login")


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "user/user-profile.html"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/user-update.html"
    success_url = reverse_lazy("user:user-profile")

    def get_object(self):
        return self.request.user


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        next_url = self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
            return next_url
        return self.request.META.get("HTTP_REFERER") or reverse_lazy("core:index")