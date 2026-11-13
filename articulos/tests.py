# articulos/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Articulo

class PruebasArticulos(TestCase):
    @classmethod
    def setUpTestData(cls):
        Usuario = get_user_model()
        cls.autora = Usuario.objects.create_user(
            username="autora", email="autora@ejemplo.mx", password="Clave-segura-2026"
        )
        cls.otro = Usuario.objects.create_user(
            username="otro", email="otro@ejemplo.mx", password="Clave-segura-2026"
        )
        cls.articulo = Articulo.objects.create(
            titulo="Un buen título", cuerpo="Texto del artículo.", autor=cls.autora
        )

    def test_modelo(self):
        self.assertEqual(str(self.articulo), "Un buen título")
        self.assertEqual(
            self.articulo.get_absolute_url(), f"/articulos/{self.articulo.pk}/"
        )

    def test_lista_publica(self):
        respuesta = self.client.get(reverse("articulo_lista"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "articulos/lista.html")
        self.assertContains(respuesta, "Un buen título")

    def test_detalle_publico(self):
        respuesta = self.client.get(self.articulo.get_absolute_url())
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Texto del artículo.")
        self.assertNotContains(respuesta, "Editar")

    def test_crear_requiere_sesion(self):
        respuesta = self.client.get(reverse("articulo_nuevo"))
        self.assertRedirects(
            respuesta, f"{reverse('login')}?next={reverse('articulo_nuevo')}"
        )

    def test_crear_asigna_autor(self):
        self.client.force_login(self.otro)
        respuesta = self.client.post(
            reverse("articulo_nuevo"), {"titulo": "Nuevo", "cuerpo": "Hola."}
        )
        nuevo = Articulo.objects.get(titulo="Nuevo")
        self.assertRedirects(respuesta, nuevo.get_absolute_url())
        self.assertEqual(nuevo.autor, self.otro)

    def test_autor_puede_editar(self):
        self.client.force_login(self.autora)
        respuesta = self.client.post(
            reverse("articulo_editar", args=[self.articulo.pk]),
            {"titulo": "Título corregido", "cuerpo": "Texto del artículo."},
        )
        self.assertRedirects(respuesta, self.articulo.get_absolute_url())
        self.articulo.refresh_from_db()
        self.assertEqual(self.articulo.titulo, "Título corregido")

    def test_otro_usuario_no_puede_editar(self):
        self.client.force_login(self.otro)
        respuesta = self.client.get(reverse("articulo_editar", args=[self.articulo.pk]))
        self.assertEqual(respuesta.status_code, 403)

    def test_otro_usuario_no_puede_eliminar(self):
        self.client.force_login(self.otro)
        respuesta = self.client.post(
            reverse("articulo_eliminar", args=[self.articulo.pk])
        )
        self.assertEqual(respuesta.status_code, 403)
        self.assertTrue(Articulo.objects.filter(pk=self.articulo.pk).exists())

    def test_autor_puede_eliminar(self):
        self.client.force_login(self.autora)
        respuesta = self.client.post(
            reverse("articulo_eliminar", args=[self.articulo.pk])
        )
        self.assertRedirects(respuesta, reverse("articulo_lista"))
        self.assertFalse(Articulo.objects.filter(pk=self.articulo.pk).exists())
