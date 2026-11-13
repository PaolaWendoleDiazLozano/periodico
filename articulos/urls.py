# articulos/urls.py
from django.urls import path

from .views import (
    VistaCrearArticulo,
    VistaDetalleArticulo,
    VistaEditarArticulo,
    VistaEliminarArticulo,
    VistaListaArticulos,
)

urlpatterns = [
    path("", VistaListaArticulos.as_view(), name="articulo_lista"),
    path("nuevo/", VistaCrearArticulo.as_view(), name="articulo_nuevo"),
    path("<int:pk>/", VistaDetalleArticulo.as_view(), name="articulo_detalle"),
    path("<int:pk>/editar/", VistaEditarArticulo.as_view(), name="articulo_editar"),
    path(
        "<int:pk>/eliminar/", VistaEliminarArticulo.as_view(), name="articulo_eliminar"
    ),
]
