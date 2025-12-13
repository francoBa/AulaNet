from django.db import models
from django.db.models import Avg, Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from math import floor

import uuid


class School(models.Model):
    SCHOOL_TYPES = [
        ("publica", "Pública"),
        ("privada", "Privada"),
        ("especial", "Especial"),
    ]
    SCHOOL_LEVEL = [
        ("primaria", "Primaria"),
        ("secundaria", "Secundaria"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    school_level = models.CharField(max_length=20, choices=SCHOOL_LEVEL)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="schools/", blank=True, default="schools/default/school-default.png"
    )

    def __str__(self):
        return self.name
    
    @property
    def rating_stars(self):
        rating = float(self.rating)

        full = floor(rating)
        half = (rating - full) >= 0.5
        empty = 5 - full - (1 if half else 0)

        return {
            "full": range(full),
            "half": half,
            "empty": range(empty),
        }
    
    def update_rating(self):
        stats = self.ratings_areas.aggregate(
            avg=Avg("average_score"),
            count=Count("id")
        )

        self.rating = stats["avg"] or 0
        self.rating_count = stats["count"] or 0
        self.save(update_fields=["rating", "rating_count"])

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.author} on {self.school}"

    
class SchoolRating(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="ratings_areas")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    pedagogica = models.JSONField()
    cultura = models.JSONField()
    bienestar = models.JSONField()
    recursos = models.JSONField()

    average_score = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("school", "user")

    def __str__(self):
        return f"{self.school.name} - {self.user.username}"

