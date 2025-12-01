from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.views import View
from django.contrib import messages


# class PostListView(ListView):
class PostListView(TemplateView):
    template_name = "blog/post-list.html"


# class PostDetailView(DetailView):
class PostDetailView(TemplateView):
    template_name = "blog/post-detail.html"


class PostDeleteView(TemplateView):
    # class PostDeleteView(DeleteView):
    template_name = "blog/post-delete.html"


class PostNewView(View):
    template_name = "blog/post-new.html"

    def get(self, request):
        # formulario vacío
        return render(request, self.template_name)

    def post(self, request):
        # 1. Obtener datos
        titulo = request.POST.get("titulo", "").strip()
        categoria = request.POST.get("categoria", "").strip()
        contenido = request.POST.get("contenido", "").strip()

        # imágenes múltiples getlist
        imagenes = request.FILES.getlist("imagenes")

        # 2. Validaciones básicas
        if not all([titulo, categoria, contenido]):
            messages.error(
                request, "El título, categoría y contenido son obligatorios."
            )
            return render(request, self.template_name)

        # 3. lógica para guardar en la Base de Datos
        # ejemplo:
        # nuevo_post = Post.objects.create(
        #     titulo=titulo,
        #     categoria=categoria,
        #     contenido=contenido,
        #     autor=request.user
        # )
        # for img in imagenes:
        #     ImagenPost.objects.create(post=nuevo_post, archivo=img)

        # 4. Mensaje de éxito
        messages.success(request, "Post publicado correctamente")

        # Redirigimos a la misma vista para que se muestre el Toast
        return redirect("blog:post-new")


class PostUpdateView(TemplateView):
    # class PostUpdateView(UpdateView):
    template_name = "blog/post-update.html"
