# articulos/urls.py
from django.urls import path

from .views import (
    VistaComentar,
    VistaCrearArticulo,
    VistaDetalleArticulo,
    VistaEditarArticulo,
    VistaEliminarArticulo,
    VistaEliminarComentario,#nuevo de los retos
    VistaListaArticulos,
    VistaMisArticulos,  # nuevo de los retos
    
)

urlpatterns = [
    path("", VistaListaArticulos.as_view(), name="articulo_lista"),
    path("mis-articulos/", VistaMisArticulos.as_view(), name="mis_articulos"),  # <-- nueva
    path("nuevo/", VistaCrearArticulo.as_view(), name="articulo_nuevo"),
    path("<int:pk>/", VistaDetalleArticulo.as_view(), name="articulo_detalle"),
    path("<int:pk>/editar/", VistaEditarArticulo.as_view(), name="articulo_editar"),
    path(
        "<int:pk>/eliminar/", VistaEliminarArticulo.as_view(), name="articulo_eliminar"),
     path("<int:pk>/comentar/", VistaComentar.as_view(), name="articulo_comentar"),  # nuevo
     path("comentario/<int:pk>/eliminar/",VistaEliminarComentario.as_view(),name="comentario_eliminar",),
]
