# cuentas/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PruebasUsuarioPersonalizado(TestCase):
    def test_crear_usuario(self):
        Usuario = get_user_model()
        usuario = Usuario.objects.create_user(
            username="ana", email="ana@ejemplo.mx", password="Clave-segura-2026", edad=20
        )
        self.assertEqual(usuario.username, "ana")
        self.assertEqual(usuario.email, "ana@ejemplo.mx")
        self.assertEqual(usuario.edad, 20)
        self.assertTrue(usuario.is_active)
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)

    def test_crear_superusuario(self):
        Usuario = get_user_model()
        admin = Usuario.objects.create_superuser(
            username="jefa", email="jefa@ejemplo.mx", password="Clave-segura-2026"
        )
        self.assertEqual(admin.username, "jefa")
        self.assertEqual(admin.email, "jefa@ejemplo.mx")
        self.assertIsNone(admin.edad)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

class PruebasRegistro(TestCase):
    def test_url_existe_en_ubicacion_correcta(self):
        respuesta = self.client.get("/cuentas/registro/")
        self.assertEqual(respuesta.status_code, 200)

    def test_vista_registro(self):
        respuesta = self.client.get(reverse("registro"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "registration/registro.html")

    def test_formulario_registro(self):
        respuesta = self.client.post(
            reverse("registro"),
            {
                "username": "lectora",
                "email": "lectora@ejemplo.mx",
                "edad": "19",
                "password1": "Clave-segura-2026",
                "password2": "Clave-segura-2026",
            },
        )
        self.assertRedirects(respuesta, reverse("login"))
        usuario = get_user_model().objects.get(username="lectora")
        self.assertEqual(usuario.email, "lectora@ejemplo.mx")
        self.assertEqual(usuario.edad, 19)