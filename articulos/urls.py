from django.urls import path

from .views import (
    ArticuloDetalleView,
    ArticuloEditarView,
    ArticuloEliminarView,
    ArticuloListaView,
    ArticuloNuevoView,
    ComentarioEliminarView,
    ComentarioPost,
    MisArticulosView,
)

urlpatterns = [
    path("<int:pk>/", ArticuloDetalleView.as_view(), name="articulo_detalle"),
    path("<int:pk>/comentar/", ComentarioPost.as_view(), name="articulo_comentar"),
    path("comentarios/<int:pk>/eliminar/", ComentarioEliminarView.as_view(), name="comentario_eliminar"),
    path("<int:pk>/editar/", ArticuloEditarView.as_view(), name="articulo_editar"),
    path("<int:pk>/eliminar/", ArticuloEliminarView.as_view(), name="articulo_eliminar"),
    path("nuevo/", ArticuloNuevoView.as_view(), name="articulo_nuevo"),
    path("mis-articulos/", MisArticulosView.as_view(), name="mis_articulos"),
    path("", ArticuloListaView.as_view(), name="articulo_lista"),
]
