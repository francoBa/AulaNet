from django.contrib import admin
from .models import School, SchoolRating
# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'school_type')
    search_fields = ('name', 'city')
    list_filter = ('school_type',)

admin.site.register(SchoolRating)
