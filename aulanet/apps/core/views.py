from apps.school.models import School
from apps.blog.models import Post
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import ContactForm


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Últimas 4 escuelas
        context["schools"] = School.objects.order_by("-id")[:4]

        # Últimos 4 posts
        context["posts"] = Post.objects.order_by("-created_at")[:4]

        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ContactForm()
        return context


class NotFoundView(TemplateView):
    template_name = "core/errors/not-found.html"


class PermissionDeniedView(TemplateView):
    template_name = "core/errors/forbidden.html"


class ServerErrorView(TemplateView):
    template_name = "core/errors/internal-error.html"


def custom_403(request, exception):
    return render(request, "core/errors/forbidden.html", status=403)


def custom_404(request, exception=None):
    return render(request, "core/errors/not-found.html", status=404)


def custom_500(request):
    return render(request, "core/errors/internal-error.html", status=500)


def contact_send(request):
    if request.method != "POST":
        return redirect(
            "core:contact"
        )  # Redirige a la página de contacto si no es POST

    form = ContactForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Por favor revisá los datos ingresados")
        return redirect("core:contact")

    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    subject = form.cleaned_data["subject"]
    message = form.cleaned_data["message"]

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "El email no es válido")
        return redirect("core:contact")

    # # Armar mensaje
    # body = f"""
    # Nuevo mensaje de contacto

    # Nombre: {name}
    # Email: {email}
    # Asunto: {subject}

    # Mensaje:
    # {message}
    # """

    # try:
    #     mail = EmailMessage(
    #         subject=f"[AulaNet] {subject}",
    #         body=body,
    #         from_email="noreply@aulanet.com",  # Cambiar según config
    #         to=["tudestino@gmail.com"],  # Adonde recibirlo
    #         reply_to=[email],
    #     )
    #     mail.send()
    # except Exception as e:
    #     return JsonResponse({"success": False, "error": "Error al enviar email"})

    messages.success(request, "Mensaje enviado correctamente")
    return redirect("core:contact")
