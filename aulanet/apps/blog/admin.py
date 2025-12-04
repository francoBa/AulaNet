from django.contrib import admin
from .models import Category, Post, Comment, PostImage
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    search_fields = ('title', 'content', 'author')
    list_filter = ('category', 'created_at')

admin.site.register(Category)

admin.site.register(Comment)

admin.site.register(PostImage)