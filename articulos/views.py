from .models import Comentario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Articulo
from .forms import ComentarioForm

class ArticuloListaView(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = "articulos/lista.html"

class ComentarioGet(DetailView):
    model = Articulo
    template_name = "articulos/detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ComentarioForm()
        return context

class ComentarioPost(SingleObjectMixin, FormView):
    model = Articulo
    form_class = ComentarioForm
    template_name = "articulos/detalle.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comentario = form.save(commit=False)
        comentario.articulo = self.object
        comentario.autor = self.request.user
        comentario.save()
        return super().form_valid(form)

    def get_success_url(self):
        articulo = self.object
        return reverse("articulo_detalle", kwargs={"pk": articulo.pk})

class ArticuloDetalleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ComentarioGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ComentarioPost.as_view()
        return view(request, *args, **kwargs)

class ArticuloEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articulo
    fields = ("titulo", "cuerpo")
    template_name = "articulos/editar.html"

    def test_func(self):
        obj = self.get_object()
        return obj.autor == self.request.user

class ArticuloEliminarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articulo
    template_name = "articulos/eliminar.html"
    success_url = reverse_lazy("articulo_lista")

    def test_func(self):
        obj = self.get_object()
        return obj.autor == self.request.user

class ArticuloNuevoView(LoginRequiredMixin, CreateView):
    model = Articulo
    template_name = "articulos/nuevo.html"
    fields = ("titulo", "cuerpo")

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class MisArticulosView(LoginRequiredMixin, ListView):
    model = Articulo
    template_name = "articulos/mis_articulos.html"

    def get_queryset(self):
        return Articulo.objects.filter(autor=self.request.user)


class ComentarioEliminarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario

    def test_func(self):
        obj = self.get_object()
        return obj.autor == self.request.user

    def get_success_url(self):
        return reverse("articulo_detalle", kwargs={"pk": self.object.articulo.pk})
