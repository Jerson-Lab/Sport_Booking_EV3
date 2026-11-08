from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Cancha, Disciplina, Perfil

from django.contrib import messages

from django.contrib.auth.decorators import(
    login_required,
    user_passes_test,
)

from django.shortcuts import redirect

from .forms import CanchaForm
from .forms import RegistroForm

from decimal import Decimal, ROUND_HALF_UP
from django.views.decorators.http import require_POST
from django.utils import timezone


from django.contrib.auth import login
from django.db import transaction



def catalogo(request):

    busqueda = request.GET.get("q","").strip()

    disciplina = request.GET.get("disciplina","").strip()

    orden = request.GET.get("orden","nombre")

    canchas = Cancha.objects.filter(
        activa=True
    ).select_related("disciplina")

    if busqueda:
        canchas = canchas.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    if disciplina:
        canchas = canchas.filter(disciplina__slug=disciplina)

    ordenamientos = {
        "nombre": "nombre",
        "precio_menor": "tarifa_hora",
        "precio_mayor": "-tarifa_hora",
    }

    canchas = canchas.order_by(
        ordenamientos.get(orden, "nombre")
    )

    paginador = Paginator(canchas, 6)

    pagina = paginador.get_page(
        request.GET.get("page")
    )

    contexto = {
        "pagina": pagina,
        "disciplinas": Disciplina.objects.all(),
        "busqueda": busqueda,
        "disciplina_seleccionada": disciplina,
        "orden": orden,
    }

    return render(
        request,
        "reservas/catalogo.html",
        contexto
    )

def detalle_cancha(request, codigo):
    cancha = get_object_or_404(
        Cancha.objects.select_related("disciplina"),
        codigo=codigo,
        activa=True
    )

    return render(
        request,
        "reservas/detalle.html",
        {"cancha": cancha}
    )

@login_required(login_url="admin:login")
@user_passes_test(
    lambda usuario: usuario.is_staff,
    login_url="admin:login"
)
def crear_cancha(request):

    if request.method == "POST":
        formulario = CanchaForm(
            request.POST,
            request.FILES
        )

        if formulario.is_valid():
            cancha = formulario.save()

            messages.success(
                request,
                "La cancha fue registrada correctamente."
            )

            return redirect(
                "cancha_detalle",
                codigo=cancha.codigo
            )
    else:
        formulario = CanchaForm()

    return render(
        request,
        "reservas/formulario_cancha.html",
        {
            "formulario": formulario,
            "titulo": "Registrar nueva cancha",
            "texto_boton": "Guardar cancha",
        }
    )

@login_required(login_url="admin:login")
@user_passes_test(
    lambda usuario: usuario.is_staff,
    login_url="admin:login"
)
def editar_cancha(request, codigo):
    cancha = get_object_or_404(
        Cancha,
        codigo=codigo,
        activa=True
    )

    if request.method == "POST":
        formulario = CanchaForm(
            request.POST,
            request.FILES,
            instance=cancha
        )

        if formulario.is_valid():
            cancha = formulario.save()

            messages.success(
                request,
                "La cancha fue actualizada correctamente."
            )
            return redirect(
                "cancha_detalle",
                codigo=cancha.codigo
            )
    else:
        formulario = CanchaForm(
            instance=cancha
        )
    return render(
        request,
        "reservas/formulario_cancha.html",
        {
                "formulario": formulario,
                "titulo": "Editar cancha",
                "texto_boton": "Guardar cambios",
        }
    )
@login_required(login_url="admin:login")
@user_passes_test(
    lambda usuario: usuario.is_staff,
    login_url="admin:login"
)
def desactivar_cancha(request, codigo):

    cancha = get_object_or_404(
        Cancha,
        codigo=codigo,
        activa=True
    )

    if request.method == "POST":

        cancha.activa = False
        cancha.save()

        messages.success(
            request,
            "La cancha fue desactivada correctamente."
        )
        return redirect("catalogo")
    return render(
        request,
        "reservas/confirmar_desactivar.html",
        {"cancha": cancha}
    )

@require_POST
def agregar_a_seleccion(request, codigo):
    cancha = get_object_or_404(
        Cancha,
        codigo=codigo,
        activa=True
    )

    if cancha.estado != Cancha.Estado.DISPONIBLE:
        messages.error(
            request,
            "Esta cancha no esta disponible."
        )

        return redirect(
            "cancha_detalle",
            codigo=codigo
        )

    try:
        horas = int (request.POST.get("horas", 1))
        personas = int(request.POST.get("personas", 1))

    except (ValueError, TypeError):
        messages.error(
            request,
            "Debes ingresar valores numéricos válidos."
        )

        return redirect(
            "cancha_detalle",
            codigo=codigo   
        )

    if not 1 <= horas <= 8:
        messages.error(
            request,
            "Debes seleccionar entre 1 y 8 horas."
        )

        return redirect(
            "cancha_detalle",
            codigo=codigo
        )

    if not 1<= personas <= cancha.capacidad:
        messages.error(
            request,
            "La cantidad de personas supera"
            "la capacidad permitida."
        )

        return redirect(
            "cancha_detalle",
            codigo=codigo   
        )

    seleccion = request.session.get(
        "seleccion_canchas",
        {}
    )

    seleccion[str(cancha.pk)] = {
        "horas": horas,
        "personas": personas,
    }
    request.session["seleccion_canchas"] = seleccion

    messages.success(
        request,
        "La cancha fue agregada a tu seleccion."
    )

    return redirect ("ver_seleccion")
def ver_seleccion(request):
    seleccion = request.session.get(
        "seleccion_canchas",
        {}
    ) 
    filas = []
    subtotal_general = Decimal (0)

    for id_cancha, datos in seleccion.items():

        cancha = Cancha.objects.filter(
            pk=id_cancha,
            activa=True
        ).first()

        if cancha is None:
            continue

        horas = datos["horas"]
        personas = datos["personas"]

        subtotal = cancha.tarifa_hora * horas

        subtotal_general += subtotal

        filas.append({
            "cancha": cancha,
            "horas": horas,
            "personas": personas,
            "subtotal": subtotal,
        })

    iva = (
        subtotal_general * Decimal("0.19")
    ).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    total = subtotal_general + iva

    contexto = {
        "filas": filas,
        "subtotal_general": subtotal_general,
        "iva": iva,
        "total": total,
    }

    return render(
        request,
        "reservas/seleccion.html",
        contexto
    )

@require_POST
def modificar_seleccion(request, codigo):

    cancha = get_object_or_404(
        Cancha,
        codigo=codigo,
        activa=True
    )

    seleccion = request.session.get(
        "seleccion_canchas",
        {}
    )

    id_cancha = str(cancha.pk)
    if id_cancha not in seleccion:
        messages.error(
            request,
            "La cancha no esta en su selección."
        )
        return redirect("ver_seleccion")

    if cancha.estado != Cancha.Estado.DISPONIBLE:
        messages.error(
            request,
            "La cancha ya no esta disponible."
        )
        return redirect("ver_seleccion")

    try:
        horas = int(request.POST.get("horas"))
        personas = int(request.POST.get("personas"))

    except (ValueError, TypeError):
        messages.error(
            request,
            "Debes ingresar valores validos."
        )
        return redirect("ver_seleccion")

    if not 1 <= horas <= 8:
        messages.error(
            request,
            "Las horas deben esta rentre 1 y 8."
        )
        return redirect("ver_seleccion")
    if not 1 <= personas <= cancha.capacidad:
        messages.error(
            request,
            "La cantidad de personas no es válida."
        )
        return redirect("ver_seleccion")

    seleccion[id_cancha] = {
        "horas": horas,
        "personas": personas,
    }

    request.session["seleccion_canchas"] = seleccion

    messages.success(
        request,
        "La selección fue actualizada correctamente."
    )

    return redirect("ver_seleccion")

@require_POST
def quitar_de_seleccion(request, codigo):

    cancha = get_object_or_404(
        Cancha,
        codigo=codigo
    )

    seleccion = request.session.get(
        "seleccion_canchas",
        {}
    )

    id_cancha = str(cancha.pk)

    if id_cancha in seleccion:

        del seleccion[id_cancha]

        request.session["seleccion_canchas"] = seleccion

        messages.success(
            request,
            "La cancha fue quitada de tu selección."
        )

    return redirect("ver_seleccion")

@require_POST
def vaciar_seleccion(request):

    request.session.pop(
        "seleccion_canchas",
        None
    )

    messages.success(
        request,
        "Tu selección fue vaciada correctamente."
    )

    return redirect("ver_seleccion")
@require_POST
def finalizar_seleccion(request):

    seleccion = request.session.get(
        "seleccion_canchas",
        {}
    )

    if not seleccion:
        messages.error(
            request,
            "No tienes canchas seleccionadas."
        )
        return redirect("ver_seleccion")

    detalle = []
    subtotal_general = Decimal("0")

    for id_cancha, datos in seleccion.items():

        cancha = Cancha.objects.filter(
            pk=id_cancha,
            activa=True,
            estado=Cancha.Estado.DISPONIBLE
        ).first()

        if cancha is None:
            messages.error(
                request,
                "Una cancha ya no esta disponible."
            )
            return redirect("ver_seleccion")

        try:
            horas = int(datos["horas"])
            personas = int(datos["personas"])

        except (ValueError, TypeError, KeyError):
            messages.error(
                request,
                "Existen datos invalidos en la seleccion."
            )
            return redirect("ver_seleccion")

        if not 1<= horas <= 8:
            messages.error(
                request,
                "La cantidad de horas no es valida"
            )
            return redirect("ver_seleccion")
        if not 1 <= personas <= cancha.capacidad:
            messages.error(
                request,
                "La cantidad de personas no es válida."
            )
            return redirect("ver_seleccion")

        subtotal = cancha.tarifa_hora * horas
        subtotal_general += subtotal

        detalle.append({
            "nombre": cancha.nombre,
            "horas": horas,
            "personas": personas,
            "subtotal": int(subtotal),
        })

    iva = (
        subtotal_general * Decimal("0.19")
    ).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )

    total = subtotal_general + iva

    comprobante = {
        "fecha": timezone.localtime().strftime(
            "%d/%m/%Y %H:%M"
        ),
        "detalle": detalle,
        "subtotal": int(subtotal_general),
        "iva": int(iva),
        "total": int(total),
    }

    request.session["ultimo_comprobante"] = comprobante

    # Vaciar únicamente la selección de canchas
    request.session.pop("seleccion_canchas", None)

    messages.success(
        request,
        "Solicitud simulada generada correctamente."
    )

    return redirect("ver_comprobante")


def ver_comprobante(request):

    comprobante = request.session.get(
        "ultimo_comprobante"
    )

    if not comprobante:
        messages.error(
            request,
            "No hay un comprobante disponible."
        )
        return redirect("ver_seleccion")

    return render(
        request,
        "reservas/comprobante.html",
        {"comprobante": comprobante}
    )

def registrar_usuario(request):

    # Evitar registrar otra cuenta con una sesión abierta
    if request.user.is_authenticated:
        return redirect("catalogo")

    if request.method == "POST":
        formulario = RegistroForm(request.POST)

        if formulario.is_valid():

            with transaction.atomic():

                usuario = formulario.save()

                Perfil.objects.create(
                    usuario=usuario,
                    rut=formulario.cleaned_data["rut"],
                    telefono=formulario.cleaned_data["telefono"],
                    rol=Perfil.Rol.CLIENTE
                )

            login(request, usuario)

            messages.success(
                request,
                "Tu cuenta fue creada correctamente."
            )

            return redirect("catalogo")

    else:
        formulario = RegistroForm()

    return render(
        request,
        "reservas/registro.html",
        {"formulario": formulario}
    )
