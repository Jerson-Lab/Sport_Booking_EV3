from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Disciplina(models.Model):
    nombre = models.CharField(
        max_length=80,
        unique=True,
    )

    slug = models.SlugField(
        max_length=80,
        unique=True,
    )

    descripcion = models.TextField(
        blank=True,
    )

    icono = models.CharField(
        max_length=6,
        default='futbol',
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'disciplina deportiva'
        verbose_name_plural = 'disciplinas deportivas'

    def __str__(self):
        return self.nombre

class Cancha(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = 'disponible', 'Disponible'
        MANTENCION = 'mantencion', 'En mantención'
        RESERVADA = 'reservada', 'Reservada'

    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.PROTECT,
        related_name='canchas',
    )

    codigo = models.SlugField(
        max_length=32,
        unique=True,
    )

    nombre = models.CharField(
        max_length=110,
    )

    descripcion = models.TextField()

    tarifa_hora = models.DecimalField(
        max_digits=9,
        decimal_places=0,
        validators=[MinValueValidator(Decimal('0'))],
    )

    capacidad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )

    estado = models.CharField(
        max_length=12,
        choices=Estado.choices,
        default=Estado.DISPONIBLE,
    )

    imagen=models.ImageField(
        upload_to='canchas/',
        blank=True,
        null=True,
    )

    activa = models.BooleanField(
        default=True,
    )

    creado_en = models.DateTimeField(
        auto_now_add=True,
    )

    actualizado_en = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'cancha'
        verbose_name_plural = 'canchas'

    def __str__(self):
        return f'{self.nombre} ({self.codigo})'

    def get_absolute_url(self):
        return reverse(
            'cancha_detalle', 
            kwargs={'codigo': self.codigo}
        )
