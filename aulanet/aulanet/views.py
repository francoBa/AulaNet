from django.views.generic import (
    FormView,
)


class AuthLoginView(FormView):
    template_name = "auth/auth-login.html"


class AuthRegisterView(FormView):
    template_name = "auth/auth-register.html"
