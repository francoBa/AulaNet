from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from datetime import date
import os

#genera nombre unico para el avatar del usuario usando su uuid
def get_avatar_filename(instance, filename):
    #asdadadadad.png
    _, file_extension = os.path.splitext(filename)
    new_filename = f"user-{instance.id}-avatar{file_extension}"
    #user/avatar/user-uuid-avatar.png
    return os.path.join("user/avatar/", new_filename)

class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city=models.CharField(max_length=120, blank=True)
    school = models.ForeignKey("school.School", null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField (max_length=50, blank=True)
    related_school = models.CharField(max_length=100, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to=get_avatar_filename, default="user/default/avatar-default.png"
    )

    @property
    def age(self):
        if not self.birthdate:
            return None

        today = date.today()
        return (
            today.year
            - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )

    
    def __str__(self):
        return self.username
    
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url