from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
import uuid
import os
from apps.school.models import School   # ← AGREGADO

# Categorías
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

# Función para generar slug único
def generate_slug(title):
    slug = slugify(title)
    unique_slug = slug
    count = 1
    while Post.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{count}"
        count += 1
    return unique_slug

# Modelo de Post
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    content = models.TextField()
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="posts"
)

    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)  # ← AGREGADO

    image = models.ImageField(upload_to='posts/cover/', blank=True, null=True, default='posts/default/post-default.jpg')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete(save=False)
        super().delete(using=using, keep_parents=keep_parents)

# Modelo de Comentarios
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="comments"
)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content

# Imágenes múltiples de Post
def get_image_filename(instance, filename):
    post_id = instance.post.id
    image_count = instance.post.images.count()
    _, file_extension = os.path.splitext(filename)
    new_filename = f"post-{post_id}-image-{image_count+1}{file_extension}"
    return os.path.join("posts/images/", new_filename)

class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_image_filename, default="posts/default/post-default.jpg")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.id)
