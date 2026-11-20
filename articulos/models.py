from django.conf import settings
from django.db import models
from django.urls import reverse

class Articulo(models.Model):
    titulo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("articulo_detalle", kwargs={"pk": self.pk})

class Comentario(models.Model):
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    comentario = models.CharField(max_length=140)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comentario

    def get_absolute_url(self):
        return reverse("articulo_lista")
