from django.db import models
from cliente.models import Cliente
from productos.models import Producto, DetalleProducto
# Create your models here.
from smart_selects.db_fields import ChainedForeignKey


class TipoPago(models.Model):
    Pago = models.CharField('Tipo de Pago', max_length=30)

    def __str__(self):
        return "%s" % (self.Pago)


class ComprobanteVenta(models.Model):
    fecha = models.DateField('Fecha de Venta')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)
    total = models.FloatField('Total', null=False, default=0.00)
    pago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, null=False)
    efectivo = models.FloatField('Efectivo', null=True, default=0.00)
    vuelto = models.FloatField('Vuelto', null=True, default=0.00)

    def __str__(self):
        return "%s %s" % (self.fecha, self.cliente)

    def save(self, *args, **kwargs):
        self.vuelto = self.efectivo - self.total
        super(ComprobanteVenta, self).save(*args, **kwargs)

    class Meta:
        db_table = 'ComprobanteVenta'
        verbose_name = 'Comprobante de Venta'
        verbose_name_plural = 'Comprobante de Ventas'


class DetalleVenta(models.Model):
    comprobante = models.ForeignKey(
        ComprobanteVenta, on_delete=models.CASCADE, null=True, blank=True,
        related_name='eldetalle')
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, null=True)
    # numlote = ChainedForeignKey(
    #    DetalleProducto,
    #    chained_field="numeroloteproducto",
    #    chained_model_field="numeroloteproducto",
    #    show_all=False,
    #    )
    cantidad = models.PositiveIntegerField('Cantidad', default=0)
    subtotal = models.FloatField(
        'subtotal', null=False, blank=False, default=0)

    class Meta:
        db_table = 'DetalleVenta'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
