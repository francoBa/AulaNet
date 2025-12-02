from django.db import models
from django.utils import timezone
import uuid
# Create your models here.

#Categoria del post
class Categoria(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.nombre

#Modelo del post
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, default="Sin categoría")
    contenido = models.TextField(null=False)
    autor = models.CharField(max_length=100, null=False)
    imagen = models.ImageField(null=True, blank=True, upload_to='media/posts/', default='media/posts/default.jpg')
    fecha = models.DateTimeField(auto_now_add = True)
    publicado = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-publicado']

    def __str__(self):
        return self.titulo
    
    def delete(self, using = None, keep_parents = False):
        self.imagen.delete(self.imagen.name)
        super().delete()
    


