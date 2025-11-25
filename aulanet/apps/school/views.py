from django.views.generic import TemplateView, CreateView, UpdateView


class CreateSchoolView(TemplateView):
    template_name = "school/create-school.html"


class ListSchoolView(TemplateView):
    template_name = "school/school-list.html"


# class UserUpdateView(UpdateView):
class ReviewSchoolView(TemplateView):
    template_name = "school/review-school.html"
