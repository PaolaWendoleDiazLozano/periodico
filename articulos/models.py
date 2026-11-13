# articulos/models.py
from django.conf import settings
from django.db import models
from django.urls import reverse


class Articulo(models.Model):
    titulo = models.CharField("título", max_length=255)
    cuerpo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "artículo"
        verbose_name_plural = "artículos"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("articulo_detalle", kwargs={"pk": self.pk})