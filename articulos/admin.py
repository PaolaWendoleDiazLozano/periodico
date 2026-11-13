# articulos/admin.py
from django.contrib import admin

from .models import Articulo


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ["titulo", "autor", "fecha"]