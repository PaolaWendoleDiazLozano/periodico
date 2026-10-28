# paginas/tests.py
from django.test import SimpleTestCase
from django.urls import reverse


class PruebasPaginaInicio(SimpleTestCase):
    def test_url_existe_en_ubicacion_correcta(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)

    def test_vista_inicio(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "inicio.html")
        self.assertContains(respuesta, "Periódico")