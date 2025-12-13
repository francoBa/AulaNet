from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminDjango
from django.contrib.auth.models import Group
from .models import User
from apps.user.models import User

# Register your models here.


class UserAdmin(UserAdminDjango):
    fieldsets = list(UserAdminDjango.fieldsets)

    fieldsets.append(
        (
            "Campos Personalizados",
            {
                "fields": (
                    "id",
                    "city",
                    "school",
                    "type",
                    "birthdate",
                    "avatar",
                    "related_school",
                ),
            },
        )
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "city",
                    "school",
                    "type",
                    "birthdate",
                    "avatar",
                    "related_school",
                )
            },
        ),
    )


def is_Registered(self, obj):
    return obj.groups.filter(name="Registered").exists()


is_Registered.short_description = "Es usuario registrado"
is_Registered.boolean = True


def is_Contributor(self, obj):
    return obj.groups.filter(name="Contributor").exists()


is_Contributor.short_description = "Es usuario colaborador"
is_Contributor.boolean = True


def is_Admin(self, obj):
    return obj.groups.filter(name="Administrador").exists()


is_Admin.short_description = "Es usuario administrador"
is_Admin.boolean = True


def add_to_Registered(self, request, queryset):
    registered_group = Group.objects.get(name="Registered")
    for user in queryset:
        user.groups.add(registered_group)
    self.message_user(
        request, "Usuarios añadidos al grupo 'Usuarios Registrados' correctamente."
    )


add_to_Registered.short_description = "Agregar al grupo 'Usuarios Registrados'"


def add_to_Contributor(self, request, queryset):
    Contributor_group = Group.objects.get(name="Contributor")
    for user in queryset:
        user.groups.add(Contributor_group)
    self.message_user(
        request, "Usuarios añadidos al grupo 'Colaborador' correctamente."
    )


add_to_Contributor.short_description = "Agregar al grupo 'Colaborador'"


def add_to_Admin(self, request, queryset):
    Admin_group = Group.objects.get(name="Admin")
    for user in queryset:
        user.groups.add(Admin_group)
    self.message_user(
        request, "Usuarios añadidos al grupo 'Administradores' correctamente."
    )


add_to_Admin.short_description = "Agregar al grupo 'Administradores'"


def remove_from_Registered(self, request, queryset):
    registered_group = Group.objects.get(name="Registered")
    for user in queryset:
        user.groups.remove(registered_group)
    self.message_user(
        request, "Usuarios eliminados del grupo 'Usuarios Registrados' correctamente."
    )


remove_from_Registered.short_description = "Eliminar del grupo 'Usuarios Registrados'"


def remove_from_Contributor(self, request, queryset):
    Contributor_group = Group.objects.get(name="Contributor")
    for user in queryset:
        user.groups.remove(Contributor_group)
    self.message_user(
        request, "Usuarios eliminados del grupo 'Colaborador' correctamente."
    )


remove_from_Contributor.short_description = "Eliminar del grupo 'Colaborador'"


def remove_from_Admin(self, request, queryset):
    Admin_group = Group.objects.get(name="Admin")
    for user in queryset:
        user.groups.remove(Admin_group)
    self.message_user(
        request, "Usuarios eliminados del grupo 'Administradores' correctamente."
    )


remove_from_Admin.short_description = "Eliminar del grupo 'Administradores'"


actions = [
    add_to_Registered,
    add_to_Contributor,
    add_to_Admin,
    remove_from_Registered,
    remove_from_Contributor,
    remove_from_Admin,
]


list_display = ("username", "email", "is_Registered", "is_Contributor", "is_Admin")

ordering = [
    "-date_joined",
]

search_fields = ["username", "email", "city", "school", "type"]

admin.site.register(User, UserAdmin)
