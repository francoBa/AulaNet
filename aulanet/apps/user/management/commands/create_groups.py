from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.blog.models import Post, Comment
from apps.school.models import School
from apps.user.models import User


class Command(BaseCommand):
    help = "Crea los grupos de usuarios (Registered, Contributor, Admin) y asigna sus permisos."

    def handle(self, *args, **options):
        self.stdout.write("⚙️  Configurando Grupos y Permisos...")

        # -----------------------------------------------------------
        # 1. CREAR OBTENER GRUPOS
        # -----------------------------------------------------------
        group_registered, _ = Group.objects.get_or_create(name="Registered")
        group_contributor, _ = Group.objects.get_or_create(name="Contributor")
        group_admin, _ = Group.objects.get_or_create(name="Admin")

        # -----------------------------------------------------------
        # 2. OBTENER CONTENT TYPES (Referencias a las tablas)
        # -----------------------------------------------------------
        ct_post = ContentType.objects.get_for_model(Post)
        ct_comment = ContentType.objects.get_for_model(Comment)
        ct_school = ContentType.objects.get_for_model(School)
        ct_user = ContentType.objects.get_for_model(User)

        # -----------------------------------------------------------
        # 3. OBTENER PERMISOS ESPECÍFICOS DE LA BD
        # -----------------------------------------------------------

        # --- Permisos de Comentarios ---
        add_comment = Permission.objects.get(
            content_type=ct_comment, codename="add_comment"
        )
        change_comment = Permission.objects.get(
            content_type=ct_comment, codename="change_comment"
        )
        delete_comment = Permission.objects.get(
            content_type=ct_comment, codename="delete_comment"
        )

        # --- Permisos de Posts (Blog) ---
        view_post = Permission.objects.get(content_type=ct_post, codename="view_post")
        add_post = Permission.objects.get(content_type=ct_post, codename="add_post")
        change_post = Permission.objects.get(
            content_type=ct_post, codename="change_post"
        )
        delete_post = Permission.objects.get(
            content_type=ct_post, codename="delete_post"
        )

        # --- Permisos de Escuelas (School) ---
        add_school = Permission.objects.get(
            content_type=ct_school, codename="add_school"
        )
        change_school = Permission.objects.get(
            content_type=ct_school, codename="change_school"
        )
        delete_school = Permission.objects.get(
            content_type=ct_school, codename="delete_school"
        )

        # --- Permisos de Usuarios (User) ---
        view_user = Permission.objects.get(content_type=ct_user, codename="view_user")
        change_user = Permission.objects.get(
            content_type=ct_user, codename="change_user"
        )
        delete_user = Permission.objects.get(
            content_type=ct_user, codename="delete_user"
        )

        # -----------------------------------------------------------
        # 4. ASIGNAR PERMISOS A LOS GRUPOS
        # -----------------------------------------------------------

        # === GRUPO: REGISTERED (Estudiantes) ===
        # Permisos: Ver posts, comentar.
        group_registered.permissions.set(
            [view_post, add_comment, change_comment, delete_comment]
        )
        self.stdout.write(f" - Grupo 'Registered' configurado (4 permisos).")

        # === GRUPO: CONTRIBUTOR (Docentes) ===
        # Permisos: Todo lo de Registered + Crear, Editar y Borrar Posts.
        group_contributor.permissions.set(
            [
                # Blog
                view_post,
                add_post,
                change_post,
                delete_post,
                # Comentarios
                add_comment,
                change_comment,
                delete_comment,
            ]
        )
        self.stdout.write(f" - Grupo 'Contributor' configurado (7 permisos).")

        # === GRUPO: ADMIN (Directores/Moderadores) ===
        # Permisos: Todo lo anterior + Gestión de Escuelas y Usuarios.
        group_admin.permissions.set(
            [
                # Blog
                view_post,
                add_post,
                change_post,
                delete_post,
                # Comentarios
                add_comment,
                change_comment,
                delete_comment,
                # Escuelas
                add_school,
                change_school,
                delete_school,
                # Usuarios
                view_user,
                change_user,
                delete_user,
            ]
        )
        self.stdout.write(f" - Grupo 'Admin' configurado (13 permisos).")

        self.stdout.write(
            self.style.SUCCESS("✅ ¡Grupos y Permisos configurados exitosamente!")
        )
