from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogo, 
         name="catalogo"),

    path("canchas/<slug:codigo>/",
         views.detalle_cancha, 
         name="cancha_detalle"),
]