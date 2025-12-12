📘 AulaNet – Plataforma para Calificar Colegios
Plataforma desarrollada con Django para calificar colegios. Conecta docentes, estudiantes y padres buscando las mejores opciones educativas para sus hijos en Resistencia (Chaco, Argentina).
Permite calificar, compartir experiencias, acceder a información útil y construir una comunidad informada para mejorar la calidad educativa.

🚀 Características principales

🏫 Directorio de Colegios de Resistencia con perfiles.

📰 Publicaciones relacionadas a los colegios divididas por categorías.

⭐ Sistema de calificaciones y valoraciones realizado por usuarios autenticados.

💬 Sección de comentarios para compartir experiencias y opiniones reales.

👤 Múltiples perfiles de usuario (administrador, colaborador y usuario registrado).

🔍 Buscador y filtros por nivel, tipo de institución y posts.

🛡️ Sistema de autenticación (login, registro, permisos).

🧩 Panel de administración Django para gestionar colegios, usuarios y contenidos.

🏗️ Tecnologías utilizadas

Backend: Django 5.x, Python 3.x

Base de datos: SQLite (desarrollo) / PostgreSQL (producción opcional)

Frontend: HTML, CSS, TailwindCSS (opcional), JavaScript


📁 Estructura del proyecto
Aulanet/
├── aulanet/                # Configuraciones generales del proyecto
├── blog/                   # App del blog (posts, categorías, comentarios)
├── schools/                # App para colegios, valoraciones, perfiles
├── users/                  # App para gestión de usuarios y autenticación
├── core/                   # App para gestión de contactos
├── static/                 # Archivos estáticos
├── templates/              # Templates globales
├── media/                  # Imágenes subidas por usuarios
└── README.md

▶️ Cómo ejecutar el proyecto (Producción en PythonAnywhere)

La versión en línea de Aulanet está desplegada en PythonAnywhere, lo que permite acceder al sitio desde cualquier navegador sin necesidad de instalar dependencias localmente.

🔗 Acceso a la plataforma

La aplicación está disponible en: [text](https://francobarreto.pythonanywhere.com/)

🔐 Roles de usuario

| Rol                    | Descripción                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| **Administrador**      | Administra colegios, usuarios, posts y categorías desde el panel |
| **Colaborador**        | Carga, edita y elimina posts y comentarios de los demás usuarios |
| **Usuario registrado** | Califica colegios, carga posts y comenta otros post de su colegio|
| **Visitante**          | Navega información pública del sitio                             |

🤝 Trabajo en equipo

Este proyecto se desarrolla de forma colaborativa. Buenas prácticas adoptadas:

Ramas: main (producción), dev (integración), feature branch

Trabajo mediante Pull Requests

Estilo PEP8

Comunicación por Discord / WhatsApp

🚧 Estado del proyecto

 Modelos iniciados (colegios, usuarios, blog)

 Sistema de calificaciones básico

 Vista de perfil de usuario

 Buscador 


🎓 Objetivo académico

Este proyecto forma parte del Proyecto Final del Informatorio 2025B - C3, cuyo propósito es:

Crear una aplicación web utilizando el framework Django y aplicando los conocimientos adquiridos durante el
curso.

👥 Integrantes del grupo

Franco Barreto
Cristian Vazquez
Martin Romero
Rocio Ramirez
Adriana Chavez