from django.contrib import admin
from .models import Categoria, Post
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    search_fields = ('title', 'content', 'author')
    list_filter = ('category', 'created_at')

admin.site.register(Categoria)