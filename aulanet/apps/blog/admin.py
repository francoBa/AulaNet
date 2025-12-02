from django.contrib import admin
from .models import Categoria, Post
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'publicado')
    search_fields = ('titulo', 'contenido', 'autor')
    list_filter = ('categoria', 'publicado')

admin.site.register(Categoria)