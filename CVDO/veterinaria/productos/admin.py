from django.contrib import admin
from . models import *
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin
from django.db.models import Count
# Register your models here.


class detalle_productoInLine(admin.TabularInline):
    readonly_fields = [
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


class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        field = ['nombre']


class ubica_Admin(admin.ModelAdmin):
    class Meta:
        model = ubicacion
        list_filter = ['ubicacionproducto']


class Producto_Admin(admin.ModelAdmin):
    list_display = ['image_img', 'nombre', 'Pro']
    list_filter = ['nombre', 'existencia']
    inlines = [detalle_productoInLine]
    resourse_class = ProductoResource
    search_fields = ['nombre']
    readonly_fields = [
        'existencia',
        ]

admin.site.register(Producto, Producto_Admin)
admin.site.register(ubicacion, ubica_Admin)
