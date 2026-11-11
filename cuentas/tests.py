# cuentas/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core import mail

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

    def test_registro_con_bootstrap(self):
        respuesta = self.client.get(reverse("registro"))
        self.assertContains(respuesta, "bootstrap.min.css")
        self.assertContains(respuesta, "form-control")

class PruebasContrasena(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username="ana", email="ana@ejemplo.mx", password="Clave-segura-2026"
        )

    def test_cambio_requiere_sesion(self):
        respuesta = self.client.get(reverse("password_change"))
        self.assertRedirects(
            respuesta, f"{reverse('login')}?next={reverse('password_change')}"
        )

    def test_cambio_de_contrasena(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(
            reverse("password_change"),
            {
                "old_password": "Clave-segura-2026",
                "new_password1": "Otra-clave-2026",
                "new_password2": "Otra-clave-2026",
            },
        )
        self.assertRedirects(respuesta, reverse("password_change_done"))
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password("Otra-clave-2026"))

    def test_reinicio_envia_correo(self):
        respuesta = self.client.post(
            reverse("password_reset"), {"email": "ana@ejemplo.mx"}
        )
        self.assertRedirects(respuesta, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["ana@ejemplo.mx"])
        self.assertIn("/cuentas/reset/", mail.outbox[0].body)

    def test_reinicio_correo_desconocido(self):
        respuesta = self.client.post(
            reverse("password_reset"), {"email": "nadie@ejemplo.mx"}
        )
        self.assertRedirects(respuesta, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

    def test_correo_personalizado(self):
        self.client.post(reverse("password_reset"), {"email": "ana@ejemplo.mx"})
        correo = mail.outbox[0]
        self.assertEqual(correo.subject, "Recupera tu contraseña del Periódico")
        self.assertIn("Hola, ana:", correo.body)
        self.assertEqual(correo.from_email, settings.DEFAULT_FROM_EMAIL)