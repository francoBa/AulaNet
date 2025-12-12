import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.utils.text import slugify
from faker import Faker
from datetime import date

# modelos
from apps.user.models import User
from apps.school.models import School, Review, SchoolRating
from apps.blog.models import Category, Post, Comment
from apps.core.models import Contact


class Command(BaseCommand):
    help = "Seeds database with real Schools (Resistencia, Chaco), Users, Contacts, Posts, etc."

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding data...")
        fake = Faker(["es_ES"])

        # 1. Limpiar datos existentes para un entorno limpio
        Post.objects.all().delete()
        School.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        Category.objects.all().delete()
        Contact.objects.all().delete()

        # 2. Asegurar Grupos
        grp_admin, _ = Group.objects.get_or_create(name="Admin")
        grp_contrib, _ = Group.objects.get_or_create(name="Contributor")
        grp_reg, _ = Group.objects.get_or_create(name="Registered")

        # 3. Crear Categorías de Blog
        categories = []
        cat_names = [
            "Noticias Institucionales",
            "Eventos",
            "Deportes",
            "Ciencia y Tecnología",
            "Arte y Cultura",
            "Comunicados",
        ]
        for name in cat_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)
        self.stdout.write(f"📚 Categories created: {len(categories)}")

        # 4. Crear Mensajes de Contacto
        self.stdout.write("✉️  Creating contact messages...")
        contact_subjects = [
            "Consulta sobre inscripción 2026",
            "Sugerencia para la plataforma",
            "Reporte de un error en la sección de noticias",
            "Pregunta sobre eventos deportivos",
            "Agradecimiento al personal docente",
        ]
        for _ in range(8):
            Contact.objects.create(
                name=fake.name(),
                email=fake.email(),
                subject=random.choice(contact_subjects),
                message=fake.text(max_nb_chars=250),
            )
        self.stdout.write(f"✉️  Created 8 contact messages.")

        # 5. Crear Colegios (Datos Reales de Resistencia, Chaco)
        school_data = [
            {
                "name": 'E.E.T. N° 21 "Gral. Manuel Belgrano" (Industrial)',
                "type": "publica",
                "level": "secundaria",
            },
            {
                "name": 'E.E.S. N° 76 "Colegio Nacional José María Paz"',
                "type": "publica",
                "level": "secundaria",
            },
            {
                "name": 'E.E.S. N° 66 "Roberto A. Muller" (Comercio N°1)',
                "type": "publica",
                "level": "secundaria",
            },
            {
                "name": 'E.E.S. N° 87 "Normal Sarmiento"',
                "type": "publica",
                "level": "secundaria",
            },
            {
                "name": 'U.E.G.P. N° 19 "Don Bosco"',
                "type": "privada",
                "level": "secundaria",
            },
            {
                "name": 'U.E.G.P. N° 172 "Gobernador A. Goitía" (Liceo)',
                "type": "privada",
                "level": "secundaria",
            },
            {
                "name": 'U.E.G.P. N° 78 "Fe y Alegría"',
                "type": "privada",
                "level": "secundaria",
            },
            {
                "name": 'E.E.P. N° 1 "Benjamín Zorrilla"',
                "type": "publica",
                "level": "primaria",
            },
            {
                "name": 'E.E.P. N° 2 "Raúl B. Díaz"',
                "type": "publica",
                "level": "primaria",
            },
            {
                "name": 'E.E.T. N° 16 "1° de Mayo"',
                "type": "publica",
                "level": "secundaria",
            },
            {
                "name": 'E.E.P. N° 33 "Independencia"',
                "type": "publica",
                "level": "primaria",
            },
            {
                "name": 'U.E.G.P. N° 23 "María Auxiliadora"',
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
                    "address": fake.address(),
                    "description": f"Prestigiosa institución educativa con una larga trayectoria en la ciudad de {fake.city()}.",
                },
            )
            schools.append(school)
            if created:
                self.stdout.write(f"🏫 Created School: {school.name}")

        COMMON_PASS = "password123"

        # 6. Crear Jerarquía de Usuarios y Contenido por cada Colegio
        for school in schools:
            self.stdout.write(f"\n--- Processing {school.name} ---")

            # A. ADMIN (Director) - 1 por colegio
            admin_username = f"admin_{slugify(school.name)[:20]}"
            self.create_user(
                username=admin_username,
                email=fake.email(),
                password=COMMON_PASS,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                school=school,
                related_school="directivo",
                group=grp_admin,
                role_name="Admin",
            )

            # B. CONTRIBUTORS (Docentes) - 2 por colegio
            for i in range(2):
                contrib_username = f"prof_{school.id.hex[:4]}_{i}"
                teacher = self.create_user(
                    username=contrib_username,
                    email=fake.email(),
                    password=COMMON_PASS,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    school=school,
                    related_school="docente",
                    group=grp_contrib,
                    role_name="Contributor",
                )

                # El docente crea 2 Posts
                teacher_posts = []
                for _ in range(2):
                    post = Post.objects.create(
                        title=fake.sentence(nb_words=6),
                        content=fake.text(max_nb_chars=800),
                        author=teacher,
                        school=school,
                        category=random.choice(categories),
                    )
                    teacher_posts.append(post)
                print(f"      📝 Created 2 posts for {teacher.username}")

                # C. REGISTERED (Estudiantes) - 3 por cada docente
                for j in range(3):
                    student_username = f"alumno_{school.id.hex[:4]}_{i}_{j}"
                    student = self.create_user(
                        username=student_username,
                        email=fake.email(),
                        password=COMMON_PASS,
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        school=school,
                        related_school="estudiante",
                        group=grp_reg,
                        role_name="Registered",
                    )

                    # El estudiante comenta en los posts de SU profesor
                    for post in teacher_posts:
                        Comment.objects.create(
                            content=fake.sentence(), author=student, post=post
                        )

                    # El primer estudiante de cada grupo deja Review y Rating a la escuela
                    if j == 0:
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
        self.stdout.write(f"🔑 All non-superuser users password: {COMMON_PASS}")

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
        # Evita duplicados
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"   👤 User {username} already exists. Skipping.")
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
            birthdate=date(
                random.randint(2005, 2008), random.randint(1, 12), random.randint(1, 28)
            ),
        )

        user.groups.add(group)
        print(f"   👤 Created {role_name}: {username}")
        return user
