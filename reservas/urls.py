from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogo, 
         name="catalogo"),

    path("canchas/<slug:codigo>/",
         views.detalle_cancha, 
         name="cancha_detalle"),
    path(
        "gestion/canchas/nueva/",
        views.crear_cancha,
        name="cancha_crear"
    ),
     path("gestion/canchas/<slug:codigo>/editar/",
          views.editar_cancha,
          name="cancha_editar"),
     path(
         "gestion/canchas/<slug:codigo>/desactivar/",
         views.desactivar_cancha,
         name="cancha_desactivar"
     ),
]