# 📘 AulaNet – **Plataforma para Calificar Colegios**
Plataforma desarrollada con Django para calificar colegios. Conecta docentes, estudiantes y padres buscando las mejores opciones educativas para sus hijos en Resistencia (Chaco, Argentina).
Permite calificar, compartir experiencias, acceder a información útil y construir una comunidad informada para mejorar la calidad educativa.


🚀 **Características principales**

🏫 Directorio de Colegios de Resistencia con perfiles.

📰 Publicaciones relacionadas a los colegios divididas por categorías.

⭐ Sistema de calificaciones y valoraciones realizado por usuarios autenticados.

💬 Sección de comentarios para compartir experiencias y opiniones reales.

👤 Múltiples perfiles de usuario (administrador, colaborador y usuario registrado).

🔍 Buscador y filtros por nivel, tipo de institución y posts.

🛡️ Sistema de autenticación (login, registro, permisos).

🧩 Panel de administración Django para gestionar colegios, usuarios y contenidos.



🏗️ **Tecnologías utilizadas**

Backend: Django 5.x, Python 3.x

Base de datos: SQLite (desarrollo) / MySQL (producción)

Frontend: HTML, CSS, TailwindCSS (opcional), JavaScript


📁 **Estructura del proyecto**
```
Aulanet/
├── aulanet/                # Configuración principal del proyecto
├── core/                   # App para gestión de contactos
├── blog/                   # Blog (posts, categorías, comentarios)
├── schools/                # Colegios, calificaciones, reseñas
├── users/                  # Autenticación y perfiles de usuario
├── static/                 # Archivos estáticos
├── templates/              # Templates globales
├── media/                  # Imágenes subidas por usuarios
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación del proyecto
```
📰 **Material de apoyo al proyecto**

El proyecto está disponible en: [Trello](https://trello.com/b/NW81mkfl/proyectofinalinformatorio)
El MER está disponible en: [Diagrams](https://app.diagrams.net/#G1YWnLF-XOxPUnNwg_EJyCvGriuzsQUq7-#%7B"pageId"%3A"dRRcaojLNauk_A8AwtsO"%7D)
El diseño está disponible en: [Figma](https://www.figma.com/design/yQzeD6InM4rgbbM6kyPs4Q/AulaNet)
El Video de presentación está disponible en: [Youtube](https://www.youtube.com/watch?v=zqP_Ryp8jbI)


▶️ **Cómo ejecutar el proyecto** (Producción en PythonAnywhere)

La versión en línea de Aulanet está desplegada en PythonAnywhere, lo que permite acceder al sitio desde cualquier navegador sin necesidad de instalar dependencias localmente.

🔗 **Acceso a la plataforma**

La aplicación está disponible en: [AulaNet](https://francobarreto.pythonanywhere.com/)

📌**Pantallas principales**

## 🔍 Buscador de colegios

<p align="center">
  <img src="https://github.com/user-attachments/assets/ccc91cc3-e874-4352-b635-ef25e4b62338" 
       alt="Buscador de colegios en Aulanet" 
       width="800">
</p>

## 🏷️ Filtro por categoría

<p align="center">
  <img src="https://github.com/user-attachments/assets/a4777196-7507-40be-8f7e-e4c0c4681182" 
       alt="Filtro de colegios por categoría" 
       width="800">
</p>

## 📩 Sección de contacto

<p align="center">
  <img src="https://github.com/user-attachments/assets/0a398ea4-73d9-4252-97a8-3d3158e41503" 
       alt="Formulario de contacto de Aulanet" 
       width="700">
</p>

## 🛠️ Administración de colegios

<p align="center">
  <img src="https://github.com/user-attachments/assets/f6bb45d2-fc53-4211-b073-0c6c27efe178" 
       alt="Panel de administración de colegios en Django" 
       width="900">
</p>

## ⭐ Sistema de calificaciones

<p align="center">
  <img src="https://github.com/user-attachments/assets/fca3508f-b705-4193-9acb-b9108aac334d" 
       alt="Sistema de calificaciones de colegios" 
       width="800">
</p>



🔐 **Roles de usuario**

| Rol                    | Descripción                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| **Administrador**      | Administra colegios, usuarios, posts y categorías desde el panel |
| **Colaborador**        | Carga, edita y elimina posts y comentarios de los demás usuarios |
| **Usuario registrado** | Califica su colegio, comenta post y edita sus comentarios|
| **Visitante**          | Navega información pública del sitio                             |


👤 **Usuarios de prueba**
Admin
USUARIO: admin_eet-n-16-1-de-mayo
CONTRASEÑA: password123

**Colaborador**
USUARIO: prof_be15_1
CONTRASEÑA: password123

**Registrado**
USUARIO: usuarioejemplo
CONTRASEÑA: password123

🤝 **Trabajo en equipo**

Este proyecto se desarrolla de forma colaborativa. Buenas prácticas adoptadas:

Ramas: main (producción), dev (integración), feature branch

Trabajo mediante Pull Requests

Estilo PEP8

Comunicación por Discord / WhatsApp



🚧 **Estado del proyecto**

 Modelos iniciados (colegios, usuarios, blog)

 Sistema de calificaciones básico

 Vista de perfil de usuario

 Buscador 



🎓 **Objetivo académico**

Este proyecto forma parte del **Proyecto Final del Informatorio 2025B - C3**, cuyo propósito es:

Crear una aplicación web utilizando el framework Django y aplicando los conocimientos adquiridos durante el
curso.


👥 **Integrantes del grupo**

Franco Barreto

Cristian Vazquez

Martin Romero

Rocio Ramirez

Adriana Chavez