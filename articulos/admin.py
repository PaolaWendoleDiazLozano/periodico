# articulos/admin.py
from django.contrib import admin

from .models import Articulo, Comentario

class ComentarioInline(admin.TabularInline):
  model = Comentario
  extra = 0

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ["titulo", "autor", "fecha"]
    inlines = [ComentarioInline]