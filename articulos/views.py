# articulos/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404  # nuevo
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import FormularioComentario  # nuevo
from .models import Articulo, Comentario  # nuevo


class VistaListaArticulos(ListView):
    model = Articulo
    template_name = "articulos/lista.html"


class VistaDetalleArticulo(DetailView):
    model = Articulo
    template_name = "articulos/detalle.html"

    def get_context_data(self, **kwargs):  # nuevo
        context = super().get_context_data(**kwargs)
        context["form"] = FormularioComentario()
        return context


class VistaComentar(LoginRequiredMixin, CreateView):  # nuevo
    model = Comentario
    form_class = FormularioComentario
    template_name = "articulos/detalle.html"
    http_method_names = ["post"]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.articulo = get_object_or_404(Articulo, pk=kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articulo"] = self.articulo
        return context

    def form_valid(self, form):
        form.instance.articulo = self.articulo
        form.instance.autor = self.request.user
        return super().form_valid(form)

    # Reto 4: redirigir directo a la sección de comentarios
    def get_success_url(self):
        return f"{self.articulo.get_absolute_url()}#comentarios"


class VistaCrearArticulo(LoginRequiredMixin, CreateView):
    model = Articulo
    fields = ["titulo", "cuerpo"]
    template_name = "articulos/nuevo.html"

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class VistaEditarArticulo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articulo
    fields = ["titulo", "cuerpo"]
    template_name = "articulos/editar.html"

    def test_func(self):
        return self.get_object().autor == self.request.user


class VistaEliminarArticulo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articulo
    template_name = "articulos/eliminar.html"
    success_url = reverse_lazy("articulo_lista")

    def test_func(self):
        return self.get_object().autor == self.request.user


# Reto 3: eliminar comentarios propios
class VistaEliminarComentario(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario
    http_method_names = ["post"]

    def test_func(self):
        return self.get_object().autor == self.request.user

    def get_success_url(self):
        return f"{self.object.articulo.get_absolute_url()}#comentarios"