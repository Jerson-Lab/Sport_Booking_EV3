from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Cancha, Disciplina
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