from django.contrib import admin

# Register your models here.
from . models import *
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin


class detalle_ventaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    readonly_fields = ['subtotal']
    autocomplete_fields = ['producto']


class comprobanteResource(resources.ModelResource):
    class Meta:
        model = ComprobanteVenta
        fields = [
            'fecha',
            'total',
            'pago'
        ]
        export_order = [
            'fecha',
            'total',
            'pago'
        ]


class ComprobanteVentaAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ['fecha', 'total']
    list_display = ['fecha', 'total', 'pago', 'vuelto']
    inlines = [detalle_ventaInline]
    resourse_class = comprobanteResource
    readonly_fields = ['total']
    # raw_id_fields = ['cliente']
    list_per_page = 10
    autocomplete_fields = ['cliente']

admin.site.register(TipoPago)
admin.site.register(ComprobanteVenta, ComprobanteVentaAdmin)
