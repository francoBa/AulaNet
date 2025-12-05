# apps/user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, LoginForm

User = get_user_model()

def auth_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido/a, {user.username}")
            return redirect(request.GET.get("next", "core:index"))
    else:
        form = LoginForm()
    return render(request, "auth/auth-login.html", {"form": form})

def auth_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect("user:login")

def auth_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Registro completado. Bienvenido/a {user.username}")
            return redirect("core:index")
    else:
        form = UserRegisterForm()
    return render(request, "auth/auth-register.html", {"form": form})

@login_required
def user_profile(request):
    # Traer últimos 10 posts y comentarios del usuario
    latest_posts = request.user.post_set.all().order_by('-created_at')[:10]
    latest_comments = request.user.comment_set.all().order_by('-created_at')[:10]
    return render(request, "user/user-profile.html", {
        "user": request.user,
        "latest_posts": latest_posts,
        "latest_comments": latest_comments,
    })

@login_required
def user_update(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("user:user-profile")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "user/user-update.html", {"form": form})
