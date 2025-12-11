import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.utils.text import slugify
from faker import Faker
from datetime import date

# Importar modelos
from apps.user.models import User
from apps.school.models import School, Review, SchoolRating
from apps.blog.models import Category, Post, Comment


class Command(BaseCommand):
    help = "Seeds database with Schools (Resistencia, Chaco), Users, Posts, Comments and Reviews"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding data...")
        fake = Faker(["es_ES"])

        # 1. Asegurar Grupos
        grp_admin, _ = Group.objects.get_or_create(name="Admin")
        grp_contrib, _ = Group.objects.get_or_create(name="Contributor")
        grp_reg, _ = Group.objects.get_or_create(name="Registered")

        # 2. Crear Categorías de Blog
        categories = []
        cat_names = ["Noticias", "Eventos", "Deportes", "Ciencia", "Arte", "Tecnología"]
        for name in cat_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)
        self.stdout.write(f"📚 Categories created: {len(categories)}")

        # 3. Crear Colegios (Datos Reales de Resistencia, Chaco)
        school_data = [
            {
                "name": 'E.E.T. N° 21 "General Manuel Belgrano" (Industrial)',
                "type": "publica",
                "level": "secundaria",
            },
            {
                "name": 'E.E.S. N° 76 "Colegio Nacional José María Paz"',
                "type": "publica",
                "level": "secundaria",
            },
            {
                "name": 'U.E.G.P. N° 19 "Don Bosco"',
                "type": "privada",
                "level": "secundaria",
            },
            {
                "name": 'E.E.P. N° 1 "Benjamín Zorrilla"',
                "type": "publica",
                "level": "primaria",
            },
            {
                "name": 'U.E.G.P. N° 16 "José Manuel Estrada"',
                "type": "privada",
                "level": "secundaria",
            },
        ]

        schools = []
        for data in school_data:
            school, created = School.objects.get_or_create(
                name=data["name"],
                defaults={
                    "school_type": data["type"],
                    "school_level": data["level"],
                    "city": "Resistencia",
                    "address": fake.address(),  # Genera una dirección aleatoria
                    "description": f"Institución educativa ubicada en Resistencia. {fake.text(max_nb_chars=100)}",
                },
            )
            schools.append(school)
            if created:
                self.stdout.write(f"🏫 Created School: {school.name}")
            else:
                self.stdout.write(f"🏫 Existing School: {school.name}")

        COMMON_PASS = "password123"

        # 4. Crear Jerarquía de Usuarios y Contenido
        for school in schools:
            self.stdout.write(f"\n--- Processing {school.name} ---")

            # A. ADMIN (Director) - 1 por colegio
            # slugify para que el username sea seguro (ej: admin_eet_n_21...)
            admin_username = (
                f"admin_{slugify(school.name)[:15]}_{random.randint(100,999)}"
            )
            self.create_user(
                username=admin_username,
                email=fake.email(),
                password=COMMON_PASS,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                school=school,
                related_school="Director",
                group=grp_admin,
                role_name="Admin",
            )

            # B. CONTRIBUTORS (Docentes) - 2 por colegio
            for i in range(2):
                contrib_username = (
                    f"prof_{school.id.hex[:4]}_{i}_{random.randint(100,999)}"
                )
                teacher = self.create_user(
                    username=contrib_username,
                    email=fake.email(),
                    password=COMMON_PASS,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    school=school,
                    related_school="Docente",
                    group=grp_contrib,
                    role_name="Contributor",
                )

                # El docente crea 3 Posts
                teacher_posts = []
                for _ in range(3):
                    post = Post.objects.create(
                        title=fake.sentence(nb_words=6),
                        content=fake.text(max_nb_chars=800),
                        author=teacher,
                        school=school,
                        category=random.choice(categories),
                        allow_comments=True,
                    )
                    teacher_posts.append(post)
                print(f"      📝 Created 3 posts for {teacher.username}")

                # C. REGISTERED (Estudiantes) - 3 por cada docente
                for j in range(3):
                    student_username = (
                        f"alumno_{school.id.hex[:4]}_{i}_{j}_{random.randint(100,999)}"
                    )
                    student = self.create_user(
                        username=student_username,
                        email=fake.email(),
                        password=COMMON_PASS,
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        school=school,
                        related_school="Estudiante",
                        group=grp_reg,
                        role_name="Registered",
                    )

                    # El estudiante comenta en los posts de SU profesor
                    for post in teacher_posts:
                        Comment.objects.create(
                            content=fake.sentence(), author=student, post=post
                        )

                    # El estudiante deja Review y Rating a la escuela
                    if j == 0:  # Solo el primero deja review para no saturar
                        Review.objects.get_or_create(
                            school=school,
                            author=student,
                            defaults={"comment": fake.text(max_nb_chars=100)},
                        )
                        SchoolRating.objects.get_or_create(
                            school=school,
                            user=student,
                            defaults={"value": random.randint(3, 5)},
                        )

        self.stdout.write(self.style.SUCCESS("\n✨ Database seeded successfully!"))
        self.stdout.write(f"🔑 All users password: {COMMON_PASS}")

    def create_user(
        self,
        username,
        email,
        password,
        first_name,
        last_name,
        school,
        related_school,
        group,
        role_name,
    ):
        if User.objects.filter(username=username).exists():
            return User.objects.get(username=username)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            school=school,
            related_school=related_school,
            city="Resistencia",
            birthdate=date(2006, 5, 20),
        )

        user.groups.clear()
        user.groups.add(group)
        user.save()

        print(f"   👤 Created {role_name}: {username}")
        return user
