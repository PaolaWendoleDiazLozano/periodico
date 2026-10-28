# cuentas/forms.py
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import UsuarioPersonalizado


class FormularioCreacionUsuario(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'edad')


class FormularioCambioUsuario(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'edad')
