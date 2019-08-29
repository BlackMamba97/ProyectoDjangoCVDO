from django.contrib import admin
from import_export.admin import ExportMixin
from . models import *
from import_export import resources


class detalle_compraInLine(admin.TabularInline):
    model = detalle_compra
    extra = 1
    readonly_fields = ['subtotal']


class ComprobanteResource(resources.ModelResource):
    class Meta:
        model = Comprobante
        fields = ['fecha', 'total', 'pago']
        export_order = ['fecha', 'total', 'pago']


class ComprobanteAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ['fecha', 'total']
    list_display = ['fecha', 'total', 'pago']
    inlines = [detalle_compraInLine]
    resourse_class = ComprobanteResource
    readonly_fields = ['total']


class PagoAdmin(admin.ModelAdmin):
    list_display = ['pago']


admin.site.register(Comprobante, ComprobanteAdmin)
admin.site.register(tipo_pago, PagoAdmin)
