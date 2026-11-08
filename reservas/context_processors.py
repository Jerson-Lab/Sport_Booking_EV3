def contador_seleccion(request):

    seleccion = request.session.get(
        "seleccion_canchas",
        {}
    )

    return{
        "contador_seleccion": len(seleccion)
    }