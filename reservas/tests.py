
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Cancha, Disciplina, Perfil


class PruebasSeguridad(TestCase):

    def setUp(self):

        Usuario = get_user_model()

        self.cliente = Usuario.objects.create_user(
            username="cliente_prueba",
            password="ClaveSegura2026!"
        )

        self.admin = Usuario.objects.create_user(
            username="admin_prueba",
            password="ClaveAdmin2026!",
            is_staff=True
        )

        disciplina = Disciplina.objects.create(
            nombre="Pádel",
            slug="padel"
        )

        self.cancha = Cancha.objects.create(
            codigo="padel-prueba",
            nombre="Pádel de prueba",
            descripcion="Cancha para pruebas",
            disciplina=disciplina,
            tarifa_hora=12000,
            capacidad=4,
            estado=Cancha.Estado.DISPONIBLE,
            activa=True
        )

    def test_cliente_no_puede_administrar(self):

        self.client.force_login(self.cliente)

        rutas = [
            reverse("cancha_crear"),
            reverse(
                "cancha_editar",
                args=[self.cancha.codigo]
            ),
            reverse(
                "cancha_desactivar",
                args=[self.cancha.codigo]
            ),
        ]

        for ruta in rutas:
            respuesta = self.client.get(ruta)
            self.assertEqual(
                respuesta.status_code,
                302
            )

    def test_admin_puede_administrar(self):

        self.client.force_login(self.admin)

        respuesta = self.client.get(
            reverse("cancha_crear")
        )

        self.assertEqual(
            respuesta.status_code,
            200
        )

    def test_inicio_y_cierre_sesion(self):

        respuesta = self.client.post(
            reverse("iniciar_sesion"),
            {
                "username": "cliente_prueba",
                "password": "ClaveSegura2026!"
            }
        )

        self.assertEqual(respuesta.status_code, 302)

        self.assertIn(
            "_auth_user_id",
            self.client.session
        )

        respuesta = self.client.post(
            reverse("cerrar_sesion")
        )

        self.assertEqual(respuesta.status_code, 302)

        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )

    def test_registro_crea_perfil_cliente(self):

        respuesta = self.client.post(
            reverse("registro"),
            {
                "username": "nuevo_cliente_prueba",
                "email": "nuevo@example.com",
                "rut": "12.345.678-5",
                "telefono": "912345678",
                "password1": "ClaveRegistro2026!",
                "password2": "ClaveRegistro2026!",
            }
        )

        self.assertEqual(respuesta.status_code, 302)

        Usuario = get_user_model()

        usuario = Usuario.objects.get(
            username="nuevo_cliente_prueba"
        )

        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)

        self.assertTrue(
            Perfil.objects.filter(
                usuario=usuario,
                rol=Perfil.Rol.CLIENTE
            ).exists()
        )
