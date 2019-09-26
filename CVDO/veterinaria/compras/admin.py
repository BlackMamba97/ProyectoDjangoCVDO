from django.contrib import admin
from import_export.admin import ExportMixin
from . models import *
from import_export import resources


class detalle_compraInLine(admin.TabularInline):
    model = detalle_compra
    extra = 1
    fields = [
        'comprobante',
        ('producto', 'numeroloteproducto'),
        'cantidad',
        'fechavencimiento',
        'ubicacion',
        ('preciocompra', 'precioventa'),
        'subtotal'
    ]
    help_text = 'Ingrese El Producto'
    readonly_fields = ['subtotal'] # , 'FechaCompra']
    autocomplete_fields = ['producto']


class ComprobanteResource(resources.ModelResource):
    class Meta:
        model = Comprobante
        fields = ['fecha', 'total', 'proveedor', 'pago']
        export_order = ['fecha', 'total', 'proveedor', 'pago']


class ComprobanteAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ['fecha', 'total']
    list_display = ['fecha', 'proveedor', 'total', 'pago']
    inlines = [detalle_compraInLine]
    fields = ['fecha', 'proveedor', ('total', 'pago')]
    resourse_class = ComprobanteResource
    readonly_fields = ['total']
    # raw_id_fields = ['proveedor']
    list_per_page = 10
    autocomplete_fields = ['proveedor']


class PagoAdmin(admin.ModelAdmin):
    list_display = ['pago']


admin.site.register(Comprobante, ComprobanteAdmin)
admin.site.register(tipo_pago, PagoAdmin)
