from django.contrib import admin
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin
# Register your models here.
from . models import *


class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
        fields = ['NIT', 'nombre', 'apellido', 'direccion', 'telefono']
        export_order = ['NIT', 'nombre', 'apellido', 'direccion', 'telefono']


class ClienteAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ['NIT', 'nombre', 'apellido']
    list_display = ['NIT', 'nombre', 'apellido', 'direccion', 'telefono']
    search_fields = ['nombre', 'NIT', 'apellido']
    resourse_class = ClienteResource
    list_per_page = 15
    ordering = ['NIT']


admin.site.register(Cliente, ClienteAdmin)
