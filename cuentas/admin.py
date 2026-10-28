from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import FormularioCambioUsuario, FormularioCreacionUsuario
from .models import UsuarioPersonalizado

# Register your models here.
@admin.register(UsuarioPersonalizado)

class UsuarioPersonalizadoAdmin(UserAdmin):
    add_form = FormularioCreacionUsuario
    form = FormularioCambioUsuario
    list_display = ['username', 'email', 'edad', 'is_staff']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ['edad']}),)
    add_fieldsets = (
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['username', 'email', 'edad', 'password1', 'password2']
            },
        ),
    )