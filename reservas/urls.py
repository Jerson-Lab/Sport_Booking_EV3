from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", views.catalogo, 
         name="catalogo"),

    path("canchas/<slug:codigo>/",
         views.detalle_cancha, 
         name="cancha_detalle"),
    path(
        "gestion/canchas/nueva/",
        views.crear_cancha,
        name="cancha_crear"),
     path("gestion/canchas/<slug:codigo>/editar/",
          views.editar_cancha,
          name="cancha_editar"),
     path(
         "gestion/canchas/<slug:codigo>/desactivar/",
         views.desactivar_cancha,
         name="cancha_desactivar"),
     
    path(
        "seleccion/",
        views.ver_seleccion,
        name="ver_seleccion"),

    path(
        "seleccion/agregar/<slug:codigo>/",
        views.agregar_a_seleccion,
        name="seleccion_agregar"),

    path(
        "seleccion/modificar/<slug:codigo>/",
        views.modificar_seleccion,
        name="seleccion_modificar"
    ),

    path(
        "seleccion/quitar/<slug:codigo>/",
        views.quitar_de_seleccion,
        name="seleccion_quitar"
    ),

    path(
        "seleccion/vaciar/",
        views.vaciar_seleccion,
        name="seleccion_vaciar"
    ),

    path(
        "seleccion/finalizar/",
        views.finalizar_seleccion,
        name="finalizar_seleccion"
    ),

    path(
        "seleccion/comprobante/",
        views.ver_comprobante,
        name="ver_comprobante"
    ),

    path(
        "cerrar-sesion/",
        LogoutView.as_view(next_page="catalogo"),
        name="cerrar_sesion"
    ),

    
    path(
        "iniciar-sesion/",
        LoginView.as_view(
            template_name="reservas/iniciar_sesion.html",
            next_page="catalogo"
        ),
        name="iniciar_sesion"
    ),
    
    path(
        "registro/",
        views.registrar_usuario,
        name="registro"
    ),

]