from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from apps.school.models import School
from apps.blog.models import Post


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        # Tomar 4 escuelas destacadas
        schools = School.objects.all()[:4]

        # Tomar 4 posts recientes
        posts = Post.objects.all().order_by('-created_at')[:4]

        context = {
            'schools': schools,
            'posts': posts,
        }
        return render(request, self.template_name, context)


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
        return redirect("core:contact")

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

    # Se comenta el envío real de email por ahora
    messages.success(request, "Mensaje enviado correctamente")
    return redirect("core:contact")
