from django.contrib import admin

from.models import Disciplina, Cancha

admin.site.site_header = "Panel de control - SportBooking"
admin.site.site_title = "SportBooking Admin"
admin.site.index_title = "Gestion de recursos y servicios deportivos"

@admin.register
class DisciplinaAdmin(admin.ModelAdmin):
    list_display =(
        'nombre',
        'slug',
        'descripcion',
    )

    search_fields = (
        'nombre',
        'slug',
        'descripcion',
    )

    prepopulated_fields = {
        'slug': ('nombre',),
    }

    ordering = ('nombre',)

@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'disciplina',
        'tarifa_hora',
        'estado',
        'activa',
    )

    list_display_links = ('nombre',)

    list_filter = (
        'disciplina',
        'estado',
        'activa',
    )

    search_fields = (
        'codigo',
        'nombre',
        'descripcion',
        'disciplina__nombre',
    )

    list_editable = (
        'tarifa_hora',
        'estado',
        'activa',
    )
    readonly_fields = (
        'creado_en',
        'actualizado_en',
    )

    fieldsets = (
        ('Información general', 
         {
            'fields': (
                'codigo',
                'nombre',
                'disciplina',
                'descripcion',
            )
        }),
        ('Tarifas y capacidad', {
            'fields': (
                'tarifa_hora',
                'capacidad',
            )
        }),
        ('Estado de la cancha', {
            'fields': (
                'estado',
                'activa',
            )
        }),
        ('Imagen de la cancha',{
            'fields': (
                'imagen',
            )
        }),
        ('Información de registros', {
            'fields': (
                'creado_en',
                'actualizado_en',
            )
        })
    )
    list_select_related = ('disciplina',)

    ordering = ('nombre',)

    list_per_page = 10