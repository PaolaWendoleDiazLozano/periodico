# articulos/urls.py
from django.urls import path

from .views import (
    VistaComentar,  # nuevo
    VistaCrearArticulo,
    VistaDetalleArticulo,
    VistaEditarArticulo,
    VistaEliminarArticulo,
    VistaListaArticulos,
    VistaEliminarComentario#nuevo de los retos
)

urlpatterns = [
    path("", VistaListaArticulos.as_view(), name="articulo_lista"),
    path("nuevo/", VistaCrearArticulo.as_view(), name="articulo_nuevo"),
    path("<int:pk>/", VistaDetalleArticulo.as_view(), name="articulo_detalle"),
    path("<int:pk>/editar/", VistaEditarArticulo.as_view(), name="articulo_editar"),
    path(
        "<int:pk>/eliminar/", VistaEliminarArticulo.as_view(), name="articulo_eliminar"),
     path("<int:pk>/comentar/", VistaComentar.as_view(), name="articulo_comentar"),  # nuevo
     path("comentario/<int:pk>/eliminar/",VistaEliminarComentario.as_view(),name="comentario_eliminar",),
]
