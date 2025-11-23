from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"


class Error404View(TemplateView):
    template_name = "core/errors/not-found.html"


class Error500View(TemplateView):
    template_name = "core/errors/internal-error.html"
