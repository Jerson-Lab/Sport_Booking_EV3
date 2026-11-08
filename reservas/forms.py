from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .models import Cancha, Perfil
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
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


class RegistroForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Correo electrónico"
    )

    rut = forms.CharField(
        max_length=12,
        required=True,
        label="RUT"
    )

    telefono = forms.CharField(
        max_length=20,
        required=True,
        label="Teléfono"
    )

    class Meta:
        model = get_user_model()

        fields = (
            "username",
            "email",
        )

        labels = {
            "username": "Nombre de usuario",
        }

    field_order = [
        "username",
        "email",
        "rut",
        "telefono",
        "password1",
        "password2",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"
    
    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        Usuario = get_user_model()

        if Usuario.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Este correo electrónico ya está registrado."
            )

        return email

    def clean_rut(self):
        rut = self.cleaned_data["rut"]

        # Quitar puntos, guiones y espacios
        rut = re.sub(r"[.\-\s]", "", rut).upper()

        if not re.fullmatch(r"\d{1,8}[\dK]", rut):
            raise forms.ValidationError(
                "El formato del RUT no es válido."
            )

        numero = rut[:-1]
        digito = rut[-1]

        # Calcular dígito verificador
        suma = 0
        multiplicador = 2

        for cifra in reversed(numero):
            suma += int(cifra) * multiplicador
            multiplicador += 1

            if multiplicador > 7:
                multiplicador = 2

        resultado = 11 - (suma % 11)

        if resultado == 11:
            verificador = "0"
        elif resultado == 10:
            verificador = "K"
        else:
            verificador = str(resultado)

        if digito != verificador:
            raise forms.ValidationError(
                "El dígito verificador del RUT es incorrecto."
            )

        rut_normalizado = f"{numero}-{digito}"

        if Perfil.objects.filter(
            rut=rut_normalizado
        ).exists():
            raise forms.ValidationError(
                "Este RUT ya se encuentra registrado."
            )

        return rut_normalizado

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()

        digitos = re.sub(r"\D", "", telefono)

        if not 8 <= len(digitos) <= 12:
            raise forms.ValidationError(
                "Ingresa un teléfono válido de 8 a 12 dígitos."
            )

        return telefono

    