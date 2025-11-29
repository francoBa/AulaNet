from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# importo la view directa para exponer un nombre no-namespaced si algún template lo pide
from apps.school.views import school_list as school_list_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Exponer nombre simple 'school-list' en el root (por compatibilidad con templates antiguos)
    path("escuela/listar/", school_list_view, name="school-list"),

    # APP ROUTES (namespaced)
    path("", include("apps.core.urls", namespace="core")),
    path("", include("apps.user.urls", namespace="user")),
    path("", include("apps.blog.urls", namespace="blog")),
    path("", include("apps.school.urls", namespace="school")),
]

# Handlers para producción
handler404 = "apps.core.views.custom_404"
handler500 = "apps.core.views.custom_500"

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
