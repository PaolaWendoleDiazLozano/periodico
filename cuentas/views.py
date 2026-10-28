from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FormularioCreacionUsuario

# Create your views here.
class VistaRegistro(CreateView):
    form_class = FormularioCreacionUsuario
    success_url = reverse_lazy('login')
    template_name = 'registration/registro.html'