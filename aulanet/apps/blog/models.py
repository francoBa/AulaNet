from django.db import models
from django.utils import timezone
import uuid
# Create your models here.

#Categoria del post
class Categoria(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.title

#Modelo del post
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False)
    category = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, default="Sin categoría")
    content = models.TextField(null=False)
    author = models.CharField(max_length=100, null=False)
    image = models.ImageField(null=True, blank=True, upload_to='media/posts/', default='media/posts/default.jpg')
    updated_at = models.DateTimeField(auto_now_add = True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def delete(self, using = None, keep_parents = False):
        self.image.delete(self.image.name)
        super().delete()
    


