from django.db import models
from django.http import Http404
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models import Sum, F
from productos.models import Producto, DetalleProducto
from django.db import transaction
import  datetime
from productos.models import ubicacion
from Proveedor.models import Proveedor


class tipo_pago(models.Model):
    pago = models.CharField('Pago', max_length=20)

    def __str__(self):
        return "%s" % (self.pago)

    class Meta:
        db_table = 'TipoPago'
        verbose_name = 'Tipo pago Compras'
        verbose_name_plural = 'Tipos de pagos de Compras'


class Comprobante(models.Model):
    # num_comprobante = models.IntegerField('num_comprobante')
    fecha = models.DateField('fecha')
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, null=True)
    total = models.FloatField('Total', null=True, default=0.00)
    pago = models.ForeignKey(tipo_pago, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "%s" % (self.proveedor)

    def save(self, *args, **kwargs):
        super(Comprobante, self).save(*args, **kwargs)

    class Meta:
        db_table = 'ComprobanteCompra'
        verbose_name = 'Comprobante de Compra'
        verbose_name_plural = 'Comprobantes de Compras'


class detalle_compra(models.Model):
    comprobante = models.ForeignKey(
        Comprobante, on_delete=models.CASCADE, null=True, blank=True,
        related_name='Eldetalle')
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE,
        null=True)
    numeroloteproducto = models.CharField(
        'Numero de lote del Producto',
        max_length=150, null=True)
    cantidad = models.PositiveIntegerField(
        'Cantidad', null=True, default=0)
    preciocompra = models.FloatField(
        'Precio Costo', null=True, blank=True, default=0.00)
    precioventa = models.FloatField(
        'Precio Venta', null=True, blank=True, default=0.00)
    fechavencimiento = models.DateField('Fecha de Vencimiento', null=False)
    ubicacion = models.ForeignKey(
        ubicacion, on_delete=models.CASCADE, null=True, blank=True)
    subtotal = models.FloatField(
        'subtotal', null=True, blank=True, default=0.00)

    def clean(self):
        if not self.pk:
            isnew = True
        else:
            isnew = False
        with transaction.atomic():
            if isnew:
                deta2 = DetalleProducto.objects.all().first()
                if deta2 is None:
                    ()
                else:
                    if self.numeroloteproducto != deta2.numeroloteproducto:
                        ()
                    else:
                        raise ValidationError(
                                    'El lote número {}'.format(
                                        self.numeroloteproducto) +
                                    ' ya existe')
        # deta2.save()

       # deta = DetalleProducto.objects.filter(
        #    producto=self.producto).last()
        #if not self.pk:
        #    isnew = True
        #else:
        #    isnew = False
        #with transaction.atomic():
        #    if isnew:
                # uno = self.lote
                # dos = deta
                #if uno != dos:
                    #raise ValidationError(
                                #'El lote número {}'.format(
                                #    uno
                                #    ) +
                                # ' no coincide con el ultimo ingresado {}'.format(
                                #     dos)
                                # )
        # deta.save()

    def save(self, force_insert=False, force_update=False, using=None):
        # deta = DetalleProducto.objects.all().last()
        self.subtotal = self.cantidad * self.preciocompra
        if not self.pk:
            isnew = True
        else:
            isnew = False

        with transaction.atomic():
            if isnew:
                # if self.numeroloteproducto != deta.numeroloteproducto or None:
                    # deta = DetalleProducto.objects.filter(
                       # producto=self.producto).last()
                    target = DetalleProducto()
                    target.producto = self.producto
                    print(self.producto)
                    target.cantidad = self.cantidad
                    target.numeroloteproducto = self.numeroloteproducto
                    target.preciocompra = self.preciocompra
                    target.precioventa = self.precioventa
                    target.fechavencimiento = self.fechavencimiento
                    # datetime.datetime.today()
                    target.ubicacion = self.ubicacion
                # else:
                    # raise ValidationError(
                    #     'El lote número {}'.format(self.numeroloteproducto) +
                    #    ' ya existe {}'.format(deta.id))
            target.save()
            super(detalle_compra, self).save(force_insert, force_update, using)
        # deta.save()
# ------------------------------Metodo para ingresar a otro detalle---------------------------

    def eliminar(self):
        detalle = DetalleProducto.objects.all()
        for i in detalle:
            if (
                i.fechavencimiento==self.fechavencimiento and i.numeroloteproducto==self.numeroloteproducto):
                    detalle = i
                    detalle.cantidad = detalle.cantidad - self.cantidad
                    print(i.numeroloteproducto)
                    print(i.cantidad)
                    print(i.producto)
                    print(i.fechavencimiento)
        detalle.save()

    def delete(self, *args, **kwargs):
        self.eliminar()
        super(detalle_compra, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'DetalleCompra'
        verbose_name = 'detalle compra'
        verbose_name_plural = 'detalle de compras'


@receiver(post_save, sender=detalle_compra)
def trigger_sumadevale(sender, **kwargs):
    linea = kwargs.get('instance')
    fact = Comprobante.objects.get(id=linea.comprobante.id)
    fact.total = fact.Eldetalle.aggregate(total=Sum(F('subtotal')))['total']
    fact.save()
