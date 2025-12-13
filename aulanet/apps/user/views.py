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
from apps.blog.models import Post, Comment



class AuthLoginView(LoginView):
    template_name = "auth/auth-login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next")

        if next_url and url_has_allowed_host_and_scheme(
            next_url, settings.ALLOWED_HOSTS
        ):
            return next_url

        return reverse_lazy("core:index")


class AuthRegisterView(CreateView):
    template_name = "auth/auth-register.html"
    form_class = RegisterForm

    def get_success_url(self):
        login_url = reverse_lazy("user:login")

        # Recuperamos el 'next' que vino del formulario (POST) o de la URL (GET)
        next_url = self.request.POST.get("next") or self.request.GET.get("next")

        # Si existe y es seguro, lo pegamos a la URL del login
        if next_url and url_has_allowed_host_and_scheme(
            next_url, settings.ALLOWED_HOSTS
        ):
            return f"{login_url}?next={next_url}"

        return login_url


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        # '?next='
        next_url = self.request.GET.get("next")

        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts=settings.ALLOWED_HOSTS,
            require_https=self.request.is_secure(),
        ):
            return next_url

        # Inicio por defecto
        return reverse_lazy("core:index")


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "user/user-profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # Últimos 5 posts del usuario
        context["user_posts"] = Post.objects.filter(author=user).order_by('-created_at')[:5]

        # Últimos 5 comentarios del usuario
        context["user_comments"] = Comment.objects.filter(author=user).order_by('-created_at')[:5]

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/user-update.html"
    success_url = reverse_lazy("user:user-profile")

    def get_object(self):
        return self.request.user
