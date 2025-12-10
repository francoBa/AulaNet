from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from apps.school.models import School
import os
import uuid
# Create your models here.

#Categoria del post
class Category(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.name



#Modelo del post
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    content = models.TextField(null=False)
    allow_comments = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default="Sin categoría")
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='posts/cover/', default='posts/default/post-default.jpg')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    @property
    def comments_count(self):
        return self.comments.count()
    
    def delete(self, using = None, keep_parents = False):
        self.image.delete(self.image.name)
        super().delete()
    
    def generate_unique_slug(self):
        """Generar un slug unico usando el titulo"""
        slug = slugify(self.title)
        unique_slug = slug
        count = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{count}"
            count += 1
        
        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

#Modelo de comentarios
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content


def get_image_filename(instance, filename):
    post_id = instance.post.id
    image_count = instance.post.images.count()
    _, file_extension = os.path.splitext(filename)
    new_filename = f"post-{post_id.id}-image-{image_count+1}{file_extension}"
    #user/avatar/post-uuid-image-1.png
    return os.path.join("post/cover/", new_filename)

class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to=get_image_filename, default=settings.POST_DEFAULT_IMAGE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"{self.id}"
