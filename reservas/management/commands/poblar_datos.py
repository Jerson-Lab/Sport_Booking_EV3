from decimal import Decimal
from getpass import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from reservas.models import Disciplina, Cancha

class Command(BaseCommand):
    help ="Carga datos iniciales para SportBooking"

    def handle(self, *args, **options):
        self.stdout.write(
            "Inicializando carga de datos para SportBooking..."
        )

        disciplinas = [
            ("futbol", "Fútbol", "Canchas de futbol", "⚽"),
            ("basquetbol", "Básquetbol", "Canchas de basquetbol", "🏀"),
            ("tenis", "Tenis", "Canchas de tenis","🎾"),
            ("padel", "Padel", "Canchas de padel", "🎾"),
            ("voleibol", "Voleibol", "Canchas de voleibol", "🏐"),
        ]

        for slug, nombre, descripcion, icono in disciplinas:

            disciplina, creada= Disciplina.objects.get_or_create(
                slug=slug,
                defaults={
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "icono": icono,
                }
            )
        if creada:
            self.stdout.write(
                f"disciplina creada: {nombre}"
            )
        canchas = [
            ("futbol-norte", "Cancha de futbol norte", "futbol", 30000, 14),
            ("futbol-sur", "Cancha de futbol sur", "futbol", 35000, 14),
            ("basquetbol-norte", "Cancha de basquetbol norte", "basquetbol", 25000, 10),
            ("tenis-centro", "Cancha de tenis centro", "tenis", 15000, 4),
            ("padel-sur", "Cancha de padel sur", "padel", 18000, 4),
            ("voleibol-sur", "Cancha de voleibol sur", "voleibol", 22000, 12),
            ("tenis-sur", "Cancha de tenis sur", "tenis", 16000, 4),
            ("padel-norte", "Cancha de pádel norte", "padel", 20000, 4),

        ]

        for codigo, nombre, slug, tarifa, capacidad in canchas:
            disciplina = Disciplina.objects.get(slug=slug)
            cancha, creada = Cancha.objects.get_or_create(
                codigo=codigo,
                defaults={
                    "nombre": nombre,
                    "disciplina": disciplina,
                    "descripcion": f"Cancha de {disciplina.nombre}.",
                    "tarifa_hora": tarifa,
                    "capacidad": capacidad,
                    "estado": Cancha.Estado.DISPONIBLE,
                    "activa": True,
                }
            )
            if creada:
                self.stdout.write(
                    f"Cancha creada: {nombre}"
                )
        self.crear_usuario("admin_demo", True)
        self.crear_usuario("cliente_demo", False)

        self.stdout.write(
            self.style.SUCCESS(
                "Carga de datos iniciales completada."
            )
        )
    def crear_usuario(self, nombre, es_admin):

        Usuario = get_user_model()
        if Usuario.objects.filter(username=nombre).exists():
            self.stdout.write(
                f"El usuario {nombre} ya existe. No se creará nuevamente."
            )
            return

        usuario_temporal = Usuario(username=nombre)

        while True:
            contraseña = getpass(f"contraseña para el usuario {nombre}: ")
            confirmacion = getpass("Repetir contraseña:")

            if contraseña != confirmacion:
                self.stderr.write("Las contraseñas no coinciden. Intente nuevamente.\n")
                continue
            try:
                validate_password(
                    contraseña, 
                    user=usuario_temporal
                )
            except ValidationError as error:
                for mensaje in error.messages:
                    self.stderr.write(f"{mensaje}\n")
                continue
            break

        Usuario.objects.create_user(
            username=nombre,
            password=contraseña,
            is_staff=es_admin,
            is_superuser=es_admin,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Usuario {nombre} creado exitosamente."
            )
        )
    