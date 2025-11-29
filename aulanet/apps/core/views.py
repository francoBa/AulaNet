from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages


class IndexView(TemplateView):
    template_name = "core/index.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"


class NotFoundView(TemplateView):
    template_name = "core/errors/not-found.html"


class ServerErrorView(TemplateView):
    template_name = "core/errors/internal-error.html"


def custom_404(request, exception=None):
    return render(request, "core/errors/not-found.html", status=404)


def custom_500(request):
    return render(request, "core/errors/internal-error.html", status=500)


def contact_send(request):
    if request.method != "POST":
        return redirect(
            "core:contact"
        )  # Redirige a la página de contacto si no es POST

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()

    if not all([name, email, subject, message]):
        messages.error(request, "Todos los campos son obligatorios")
        return redirect("core:contact")

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
