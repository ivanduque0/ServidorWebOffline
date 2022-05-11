from django.contrib import admin
from .models import contratos, fotos, interacciones, usuarios
# Register your models here.

class contratosadmin(admin.ModelAdmin):

    fieldsets = [
        #a la izquierda se pone como se quiere que se llame todo el formulario, y a la derecha se ponen los
        #nombres de los field en la clase
        ("agregar contrato", {'fields': ['nombre']}),

    ]

class interaccionesadmin(admin.ModelAdmin):

    fieldsets = [
        ("Historico de actividad", {'fields': ['cedula','nombre','fecha','hora','razon', 'contrato']}),
    ]

class usuariosadmin(admin.ModelAdmin):

    fieldsets = [
        ("usuario", {'fields': ['cedula','nombre','contrato']}),
    ]

admin.site.register(contratos, contratosadmin)
admin.site.register(usuarios,usuariosadmin)
admin.site.register(interacciones, interaccionesadmin)
admin.site.register(fotos)