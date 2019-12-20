from django.contrib import admin

# Register your models here.
from . models import *
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin
from usuarios.models import Empleado
from django.shortcuts import redirect


class detalle_ventaInline(admin.TabularInline):
    model = DetalleVenta
    fields = [
        'producto',
        'numeroloteproducto',
        'cantidad',
        'subtotal'
            ]
    extra = 1
    readonly_fields = [
        'comis',
        'subtotal',
    ]
    autocomplete_fields = ['producto']

    # def get_formset_kwargs(self, request, obj, form, change):
    #    print('Si entro a detalle')
    #    det = DetalleProducto.objects.filter(
    #        producto=self.producto).exclude(
    #        cantidad=0).last()
    #    if det.fechavencimiento > date.today() and det.numeroloteproducto==self.numeroloteproducto:
    #        formset_kwargs = messages.info(
    #            request, 'Este lote es el adecuado.')
    #    return formset_kwargs


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
    # se crea la clase comprobanteventa para
    fields = ['fecha', (
        'cliente', 'pagado'), 'vendedor', 'pago', 'total', 'efectivo', 'vuelto']
    list_filter = ['fecha', 'vendedor']
    list_display = ['fecha', 'vendedor', 'total', 'pagado', 'pago', 'vuelto', 'compro']
    inlines = [detalle_ventaInline]
    resourse_class = comprobanteResource
    readonly_fields = ['total', 'vuelto']
    # raw_id_fields = ['cliente']
    list_per_page = 15
    ordering = ['-fecha']
    actions = ['impr_prods']
    autocomplete_fields = ['cliente']

    def get_form(self, request, *args, **kwargs):
        form = super(ComprobanteVentaAdmin, self).get_form(
            request, *args, **kwargs)
        usuario = request.user
        # empleado = Empleado.objects.filter(Empleado=usuario.id)
        form.base_fields['vendedor'].initial = usuario
        return form

    def save_model(self, request, obj, form, change):
        print('Si entro al compobante')
        messages.info(
            request, (
                'Asegurese de ingresar siempre el producto proximo a venceser.'
                ))
        super(
            ComprobanteVentaAdmin, self).save_model(request, obj, form, change)

    def impr_prods(self, request, queryset):
        return redirect('/InformeVentas')
    impr_prods.short_description = 'Exportar ventas'

admin.site.register(TipoPago)
admin.site.register(ComprobanteVenta, ComprobanteVentaAdmin)
