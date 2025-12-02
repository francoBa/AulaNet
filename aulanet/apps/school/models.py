from django.db import models
from django.contrib.auth.models import User
import uuid

class School(models.Model):
    SCHOOL_TYPES = [
        ('publica', 'Pública'),
        ('privada', 'Privada'),
        ('especial', 'Especial'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=120)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='schools/', blank=True, null=True)


class SchoolRating(models.Model):
    school = models.ForeignKey(
        School,
        related_name='ratings',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school', 'user')

    def __str__(self):
        return f"{self.school.name} - {self.value}★"
