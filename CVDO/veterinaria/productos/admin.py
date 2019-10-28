from django.contrib import admin
from . models import *
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin
from django.db.models import Count
from django.shortcuts import redirect
# Register your models here.


class detalle_productoInLine(admin.TabularInline):
    # se crea la clase de detalle producto
    # con el atributo tabularInline para mantener la forma de
    # el despliegue
    readonly_fields = [
        # especificamos que todos estos atributos solo serán de lectura
        'FechaCompra',
        'cantidad',
        'numeroloteproducto',
        'preciocompra',
        'precioventa',
        'fechavencimiento',
        'ubicacion',
        'fechaq',
        'estadoo',
    ]
    model = DetalleProducto
    extra = 0
    ordering = ['fechavencimiento']
    # se estipula que todos los detalles se oldenarán por medio de
    # la fecha de vencimiento


class ProductoResource(resources.ModelResource):
    # creación de la clase para Resource de Productos
    class Meta:
        model = Producto
        field = ['nombre']


class ubica_Admin(admin.ModelAdmin):
    #creación de la clase ubicación en el admin
    class Meta:
        model = ubicacion
        list_filter = ['ubicacionproducto']


class tipop_Admin(admin.ModelAdmin):
    # creación de clase Tipo de Producto en el admin
    class Meta:
        model = tipoproducto
        list_filter = ['TipoProducto']


class Producto_Admin(admin.ModelAdmin):
    # creación de clase Producto en el admin
    list_display = ['image_img', 'nombre', 'tipoProducto', 'Pro']
    # se definen los atributos de Producto que se van a mostrar en el listado
    list_filter = ['nombre', 'tipoProducto']
    # Se definen los atributos por los cuales se van a buscar los productos
    inlines = [detalle_productoInLine]
    # se define que tendra un atributo de tipo InLine en su modelo
    resourse_class = ProductoResource
    search_fields = ['nombre']
    # se define que solo se podrán buscar articulos por medio de nombre
    list_per_page = 15
    # se define que solo se podrán desplegar 5 elementos de la lista
    # y despues se crearán pestallas
    # actions = [
    #    'impr_prods',
    #    'impr_prodofer',
    #    'impr_prodorden',
    # ]
    readonly_fields = [
        # el unico atributo que sera de lectura seran las existencias
        'existencia',
        ]

    def impr_prods(self, request, queryset):
        return redirect('/InformedeProductosVencidos')
    impr_prods.short_description = 'Productos Vencidos'

    def impr_prodofer(self, request, queryset):
        return redirect('/InformedeProductosdeOfertas')
    impr_prodofer.short_description = 'Productos a Ofertar'

    def impr_prodorden(self, request, queryset):
        return redirect('/InformedeProductosenOrden')
    impr_prodorden.short_description = 'Productos en Orden'


class DetalleProducto_Empleado_Admin(admin.TabularInline):
    fields = [
        'FechaCompra',
        'cantidad',
        'numeroloteproducto',
        'precioventa',
        'fechavencimiento',
        'ubicacion',
        'fechaq',
        'estadoo',
    ]
    readonly_fields = [
        'FechaCompra',
        'cantidad',
        'numeroloteproducto',
        'precioventa',
        'fechavencimiento',
        'ubicacion',
        'fechaq',
        'estadoo',
    ]
    model = DetalleProducto_Empleado
    extra = 0
    ordering = ['fechavencimiento']


class Productos_Empleado_Admin(admin.ModelAdmin):
    list_display = ['image_img', 'nombre', 'Pro']
    list_filter = ['nombre', 'tipoProducto']
    inlines = [DetalleProducto_Empleado_Admin]
    # resourse_class = ProductoResource
    fields = [
        'image_img',
        'existencia',
        'nombre',
    ]
    search_fields = ['nombre']
    list_per_page = 15
    readonly_fields = [
        'meses',
        'image',
        'image_img',
        'nombre',
        'existencia',
        ]

admin.site.register(Producto, Producto_Admin)
admin.site.register(tipoproducto, tipop_Admin)
admin.site.register(ubicacion, ubica_Admin)
# admin.site.register(DetalleProducto_Empleado, DetalleProducto_Empleado_Admin)
admin.site.register(Productos_Empleado, Productos_Empleado_Admin)
# admin.site.register(NumeroLote, Numero_Admin)
