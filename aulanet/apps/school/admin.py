from django.contrib import admin
from .models import School, SchoolRating, Review 
# Register your models here.


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'school_type')
    search_fields = ('name', 'city')
    list_filter = ('school_type',)

admin.site.register(School, SchoolAdmin)

admin.site.register(SchoolRating)

admin.site.register(Review)
