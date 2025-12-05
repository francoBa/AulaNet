from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
import uuid

def generate_school_slug(name):
    slug = slugify(name)
    unique_slug = slug
    count = 1
    while School.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{count}"
        count += 1
    return unique_slug

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
    MANAGEMENT_TYPES = [
        ('publica', 'Pública'),
        ('privada', 'Privada'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)  # ← AGREGADO

    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    school_level = models.CharField(max_length=20, choices=SCHOOL_LEVEL)
    management_type = models.CharField(max_length=20, choices=MANAGEMENT_TYPES, blank=True, null=True)

    number = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='schools/', blank=True, null=True)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_schools",
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_school_slug(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/school/{self.slug}/"

    def __str__(self):
        return self.name

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class SchoolRating(models.Model):
    school = models.ForeignKey(School, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school', 'user')

    def __str__(self):
        return f"{self.school.name} - {self.value}★"
