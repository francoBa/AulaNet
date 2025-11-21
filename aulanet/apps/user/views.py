from django.views.generic import TemplateView, UpdateView


class UserProfileView(TemplateView):
    template_name = "user/user-profile.html"


class UserUpdateView(UpdateView):
    template_name = "user/user-update.html"
