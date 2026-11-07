from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .models import Cancha

class CanchaForm(forms.ModelForm):

    class Meta:
        model = Cancha

        fields = [
            "codigo",
            "nombre",
            "disciplina",
            "descripcion",
            "tarifa_hora",
            "capacidad",
            "estado",
            "imagen",
        ]

        labels = {
            "codigo": "Código de la cancha",
            "nombre": "Nombre de la cancha",
            "disciplina": "Disciplina deportiva",
            "descripcion": "Descripción",
            "tarifa_hora": "Precio por hora ($)",
            "capacidad": "Capacidad de personas",
            "estado": "Estado de la cancha",
            "imagen": "Imagen de la cancha",
        }

        widgets = {
            "codigo": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "nombre": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "disciplina": forms.Select(
                attrs={"class": "form-select"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "tarifa_hora": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
            "capacidad": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "estado": forms.Select(
                attrs={"class": "form-select"}
            ),
            "imagen": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }
    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo")

        if not codigo:
            return codigo

        canchas = Cancha.objects.filter(
            codigo__iexact=codigo
        )

        if self.instance.pk:
            canchas = canchas.exclude(
                pk=self.instance.pk
            )

        if canchas.exists():
            raise ValidationError(
                "Ya existe una cancha con este código."
            )

        return codigo

    def clean_tarifa_hora(self):
        tarifa = self.cleaned_data.get("tarifa_hora")

        if tarifa is not None and tarifa < Decimal ("0"):
            raise ValidationError(
                "El precio no puede ser negativo"
            )
        return tarifa

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get("capacidad")

        if capacidad is not None and capacidad < 1:
            raise ValidationError(
                "La capacidad debe ser al menos 1 persona"
            )
        return capacidad
    