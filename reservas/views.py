from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Cancha, Disciplina

from django.contrib import messages

from django.contrib.auth.decorators import(
    login_required,
    user_passes_test,
)

from django.shortcuts import redirect

from .forms import CanchaForm
# Create your views here.

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
