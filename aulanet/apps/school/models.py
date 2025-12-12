from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify

import uuid

class School(models.Model):
    SCHOOL_TYPES = [
        ('publica', 'Pública'),
        ('privada', 'Privada'),
        ('especial', 'Especial'),
    ]
    SCHOOL_LEVEL = [
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    school_level = models.CharField(max_length=20, choices=SCHOOL_LEVEL)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='schools/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            # asegurar que el slug sea único
            while School.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)



class Review(models.Model):
    id = id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name= 'reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now = True)
    


class SchoolRating(models.Model):
    school = models.ForeignKey(
        School,
        related_name='ratings',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school', 'user')

    def __str__(self):
        return f"{self.school.name} - {self.value}★"
