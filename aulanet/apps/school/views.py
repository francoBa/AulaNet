from django.views.generic import TemplateView, CreateView, UpdateView


class CreateSchoolView(TemplateView):
    template_name = "school/create-school.html"


class ListSchoolView(TemplateView):
    template_name = "school/school-list.html"


# class UserUpdateView(UpdateView):
class ReviewSchoolView(TemplateView):
    template_name = "school/review-school.html"

class SchoolDetailView(TemplateView):
    template_name = "school/school-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        context["school_id"] = pk  # para usar en el template
        return context