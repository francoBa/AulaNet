from django.shortcuts import render
from django.views.generic import TemplateView


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
