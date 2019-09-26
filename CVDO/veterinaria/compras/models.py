from django.db import models
from django.http import Http404
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models import Sum, F
from productos.models import Producto, DetalleProducto
from django.db import transaction
from datetime import date
from productos.models import ubicacion
from Proveedor.models import Proveedor
# from django.utils import timezone
# from django.utils import timezone


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
    fecha = models.DateField('fecha', default=date.today)
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
    now = date.today
    comprobante = models.ForeignKey(
        Comprobante, on_delete=models.CASCADE, null=True, blank=True,
        related_name='Eldetalle')
    FechaCompra = models.DateField(
        'Fecha de Compra', default=now)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE,
        null=True)
    numeroloteproducto = models.CharField(
       'Numero de lote',
       max_length=20, null=True, blank=True)
    # numeroloteproducto = models.ForeignKey(
    #    NumeroLote, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(
        'Cantidad', null=True, default=0)
    preciocompra = models.FloatField(
        'Precio Costo', null=False, blank=False, default=0.00)
    precioventa = models.FloatField(
        'Precio Venta', null=False, blank=False, default=0.00)
    fechavencimiento = models.DateField(
        'Fecha de Vencimiento', null=True, blank=True)
    ubicacion = models.ForeignKey(
        ubicacion, on_delete=models.CASCADE, null=False, blank=False)
    subtotal = models.FloatField(
        'subtotal', null=True, blank=True, default=0.00)

    # def clean(self):
    #    if not self.pk:
    #        isnew = True
    #    else:
    #        isnew = False
    #    with transaction.atomic():
    #        if isnew:
    #            detalle = DetalleProducto.objects.all()
    #            for i in detalle:
    #                detalle = i
    #                if(detalle.numeroloteproducto != self.numeroloteproducto):
    #                    ()
    #                else:
    #                    raise ValidationError(
    #                                'El lote número {}'.format(
    #                                    self.numeroloteproducto) +
    #                                ' ya existe')
    #        else:
    #            ()
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
                #deta = DetalleProducto.objects.filter(
                 #      producto=self.producto).last()
                #if self.numeroloteproducto != deta.numeroloteproducto or None:
                if self.fechavencimiento is None:
                    targe = DetalleProducto.objects.filter(producto=self.producto).last()
                    if targe is None:
                        target = DetalleProducto()
                        target.producto = self.producto
                        target.cantidad = self.cantidad
                        target.FechaCompra = self.FechaCompra
                        target.preciocompra = self.preciocompra
                        target.precioventa = self.precioventa
                        target.numeroloteproducto = self.numeroloteproducto
                        # target.fechavencimiento == self.fechavencimiento
                        # target.cantidad = target.cantidad + self.cantidad
                        target.ubicacion = self.ubicacion
                        target.save()
                    else:
                        if self.preciocompra == targe.preciocompra and self.precioventa == targe.precioventa:
                            targe.cantidad = targe.cantidad + self.cantidad
                            targe.save()
                        else:
                            target = DetalleProducto()
                            target.producto = self.producto
                            target.cantidad = self.cantidad
                            target.FechaCompra = self.FechaCompra
                            target.preciocompra = self.preciocompra
                            target.precioventa = self.precioventa
                            target.numeroloteproducto = self.numeroloteproducto
                            # target.fechavencimiento == self.fechavencimiento
                            #target.cantidad = target.cantidad + self.cantidad
                            target.ubicacion = self.ubicacion
                            target.save()
                    # target.save()
                    # targe.save()
                else:
                    target = DetalleProducto()
                    target.producto = self.producto
                    # print(self.producto)
                    target.FechaCompra = self.FechaCompra
                    target.cantidad = self.cantidad
                    target.numeroloteproducto = self.numeroloteproducto
                    target.preciocompra = self.preciocompra
                    target.precioventa = self.precioventa
                    # if self.fechavencimiento == "":
                    #    ()
                    # else:
                    target.fechavencimiento = self.fechavencimiento
                    # datetime.datetime.today()
                    target.ubicacion = self.ubicacion

                    # target.save()importante
                    # estas son pruebas de save()
                    target.save()
                    # targe.save()
            else:
                ()
                    #raise ValidationError(
                    #    'El lote número {}'.format(self.numeroloteproducto) +
                    #        ' ya existe')
            super(detalle_compra, self).save(force_insert, force_update, using)
        # deta.save()
# ------------------------------Metodo para ingresar a otro detalle---------------------------

    def eliminar(self):
        detalle = DetalleProducto.objects.all()
        for i in detalle:
            if (
                i.FechaCompra==self.FechaCompra and i.preciocompra==self.preciocompra and i.precioventa==self.precioventa or i.numeroloteproducto==self.numeroloteproducto and i.preciocompra==self.preciocompra and i.precioventa==self.precioventa):
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
