from django.contrib import admin

# Register your models here.
from . models import *
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin
from usuarios.models import Empleado


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
            'pago',
            'vendedor',
        ]
        export_order = [
            'fecha',
            'total',
            'pago',
            'vendedor',
        ]


class ComprobanteVentaAdmin(ExportMixin, admin.ModelAdmin):
    list_filter = ['fecha', 'total', 'vendedor']
    list_display = ['fecha', 'vendedor', 'total', 'pago', 'vuelto', 'compro']
    inlines = [detalle_ventaInline]
    resourse_class = comprobanteResource
    readonly_fields = ['total']
    # raw_id_fields = ['cliente']
    list_per_page = 10
    autocomplete_fields = ['cliente']

    def get_form(self, request, *args, **kwargs):
        form = super(ComprobanteVentaAdmin, self).get_form(
            request, *args, **kwargs)
        usuario = request.user
        # empleado = Empleado.objects.filter(Empleado=usuario.id)
        form.base_fields['vendedor'].initial = usuario
        return form

admin.site.register(TipoPago)
admin.site.register(ComprobanteVenta, ComprobanteVentaAdmin)
