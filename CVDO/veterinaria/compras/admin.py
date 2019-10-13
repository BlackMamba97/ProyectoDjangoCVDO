from django.contrib import admin
from import_export.admin import ExportMixin
from . models import *
from import_export import resources


class detalle_compraInLine(admin.TabularInline):
    # se crea el detalle compra en el archivo admin.py
    model = detalle_compra
    extra = 1
    # se agrega una linea extra para ingresar el detalle
    fields = [
        # se definen los atributos que ingresara el usuario
        'comprobante',
        ('producto', 'numeroloteproducto'),
        'cantidad',
        'fechavencimiento',
        'ubicacion',
        ('preciocompra', 'precioventa'),
        'subtotal'
    ]
    # help_text = 'Ingrese El Producto'
    readonly_fields = ['subtotal']
    # subtotal será el unico atributo que será de solo lectura
    # ya que subtotal es un atributo generado por el sistema
    autocomplete_fields = ['producto']
    # este comando sirve para autogenerar las palabras


class ComprobanteResource(resources.ModelResource):
    class Meta:
        model = Comprobante
        fields = ['fecha', 'total', 'proveedor', 'pago']
        export_order = ['fecha', 'total', 'proveedor', 'pago']


class ComprobanteAdmin(ExportMixin, admin.ModelAdmin):
    # creacion de la clase comprobante admin
    list_filter = ['fecha', 'total']
    # se crea el listado de filtraciones
    list_display = ['fecha', 'proveedor', 'total', 'pago', 'compro']
    # se crea el listado de despliegue
    fields = ['fecha', 'proveedor', 'pago', 'total']
    inlines = [detalle_compraInLine]
    resourse_class = ComprobanteResource
    readonly_fields = ['total']
    # el unico atributo de lectura será total
    # raw_id_fields = ['proveedor']
    list_per_page = 15
    autocomplete_fields = ['proveedor']
    # se genera el autocompletado para ingresar los proveedores


class PagoAdmin(admin.ModelAdmin):
    # crea la clase de pago
    list_display = ['pago']


admin.site.register(Comprobante, ComprobanteAdmin)
admin.site.register(tipo_pago, PagoAdmin)
