from django.contrib import admin
from .models import Category, Post, Comment, PostImage
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at',
                    'updated_at', 'allow_comments')
    search_fields = ('title', 'content',
                     'author__username', 'author__id', 'id')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('created_at', 'allow_comments')
    ordering = ('-created_at',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(Comment)

admin.site.register(PostImage)