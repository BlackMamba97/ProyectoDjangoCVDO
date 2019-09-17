from django.contrib import admin
from import_export.admin import ExportMixin
from . models import *
from import_export import resources
# Register your models here.


class ProveedorResource(resources.ModelResource):
    class Meta:
        model = Proveedor
        fields = ['codigo', 'nombre', 'direccion']
        export_order = ['fecha', 'total', 'pago']


class ProveedorAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ['nombre']
    list_display = ['nombre', 'telefono', 'direccion']
    search_fields = ['nombre']
    resourse_class = ProveedorResource

admin.site.register(Proveedor, ProveedorAdmin)
