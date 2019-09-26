from django.db import models
from cliente.models import Cliente
from productos.models import Producto, DetalleProducto
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models import Sum, F
from django.db.models.signals import post_save
from usuarios.models import Empleado
from datetime import date
# Create your models here.
# from smart_selects.db_fields import ChainedForeignKey
# from smart_selects.db_fields import GroupedForeignKey


class TipoPago(models.Model):
    Pago = models.CharField('Tipo de Pago', max_length=30)

    def __str__(self):
        return "%s" % (self.Pago)


class ComprobanteVenta(models.Model):
    fecha = models.DateField('Fecha de Venta', default=date.today)
    #cliente = models.ForeignKey(
    #     Cliente, on_delete=models.CASCADE, null=False)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=False)
    total = models.FloatField('Total', null=True, default=0.00)
    pago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, null=False)
    efectivo = models.FloatField('Efectivo', null=True, default=0.00)
    vuelto = models.FloatField('Vuelto', null=True, default=0.00)
    vendedor = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "%s %s" % (self.fecha, self.cliente)

    # def comisi(self):
    #    ven = Empleado.objects.filter(Empleado=self.vendedor)
    #        ven.comision = ven.comision + ()

    def save(self, *args, **kwargs):
        self.vuelto = self.efectivo - self.total
        super(ComprobanteVenta, self).save(*args, **kwargs)

    def compro(self):
        return mark_safe(
            u'<a href="/comprobanteventa/?id=%s" target="_blank">Comprobante</a>' % self.id)
    compro.short_description = 'Comprobante de Venta'

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
    numeroloteproducto = models.CharField(
       'Numero de lote',
       max_length=20, null=True, blank=True)
    cantidad = models.PositiveIntegerField('Cantidad', default=0)
    comis = models.FloatField('Comision', default=0)
    subtotal = models.FloatField(
        'subtotal', null=False, blank=False, default=0)

    def preciov(self):
        precio = self.subtotal/self.cantidad
        return precio

    def clean(self):
        prode = DetalleProducto.objects.filter(
                producto=self.producto).first()
        det = DetalleProducto.objects.filter(
            producto=self.producto).all()
        pro = Producto.objects.filter(
                        nombre=self.producto.nombre).get()
        if prode.fechavencimiento is None:
            for i in det:
                de = i
                if de.cantidad > 0:
                    if self.cantidad > pro.existencia:
                        raise ValidationError(
                            ' No tenemos en existencia{}'.format(
                                self.cantidad) +
                            ' solo contamos con {}'.format(
                                pro.existencia))
                    else:
                        if de.cantidad >= self.cantidad:
                            ()
                        else:
                            raise ValidationError(
                                ' Verifique las existencias ya que varían los precios de {}'.format(
                                    de.producto))
                else:
                    ()
        else:
            if self.numeroloteproducto is None:
                        raise ValidationError(
                            ' Este Producto necesita ingresar Numero de Lote para ser vendido')
            else:
                prod = DetalleProducto.objects.filter(
                    numeroloteproducto=self.numeroloteproducto).get()
                pro = Producto.objects.filter(
                    nombre=self.producto.nombre).get()
                if pro.existencia >= self.cantidad:
                    if prod.cantidad >= self.cantidad:
                        ()
                    else:
                        raise ValidationError(
                            'Este numero de lote solo cuenta con {}'.format(
                                prod.cantidad) + ' unidades')
                else:
                    raise ValidationError(
                        ' No tenemos en existencia {}'.format(
                            self.cantidad) +
                        ' solo contamos con {}'.format(
                            pro.existencia))

    def save(self, force_insert=False, force_update=False, using=None):
        prode = DetalleProducto.objects.filter(
                producto=self.producto).first()
        if not self.pk:
            isnew = True
        else:
            isnew = False

        with transaction.atomic():
            if isnew:
                if prode.fechavencimiento is None:
                    det = DetalleProducto.objects.filter(
                        producto=self.producto).all()
                    pro = Producto.objects.filter(
                        nombre=self.producto.nombre).get()
                    if pro == self.producto:
                        for i in det:
                            de = i
                            if de.cantidad > 0:
                                if self.cantidad > pro.existencia:
                                    ()
                                else:
                                    if de.cantidad >= self.cantidad:
                                        de.cantidad = (
                                            de.cantidad - self.cantidad)
                                        self.subtotal = (
                                            self.cantidad * de.precioventa)
                                        self.comis = (
                                            self.cantidad * de.precioventa * (
                                                pro.porcentaje/100))
                                        emp = Empleado.objects.filter(
                                            Empleado=self.comprobante.vendedor.id).get()
                                        print('---------------')
                                        print(emp.comision)
                                        print(emp)
                                        emp.comision = emp.comision + self.comis
                                        emp.save()
                                        de.save()
                                    else:
                                        ()
                            else:
                                ()
                else:
                    if self.numeroloteproducto is None:
                        ()
                    else:
                        prod = DetalleProducto.objects.filter(
                            numeroloteproducto=self.numeroloteproducto).get()
                        pro = Producto.objects.filter(
                            nombre=self.producto.nombre).get()
                        if pro.existencia >= self.cantidad:
                            if prod.cantidad >= self.cantidad:
                                prod.cantidad = (prod.cantidad - self.cantidad)
                                self.subtotal = self.cantidad * prod.precioventa
                                self.comis = (
                                    self.cantidad * prod.precioventa * (
                                        pro.porcentaje/100))
                                emp = Empleado.objects.filter(
                                    Empleado=self.comprobante.vendedor.id).get()
                                print('---------------')
                                print(emp.comision)
                                print(emp)
                                emp.comision = emp.comision + self.comis
                                emp.save()
                                prod.save()
                            else:
                                ()
                        else:
                            ()
        super(DetalleVenta, self).save(force_insert, force_update, using)

    class Meta:
        db_table = 'DetalleVenta'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'


@receiver(post_save, sender=DetalleVenta)
def trigger_sumadevale(sender, **kwargs):
    linea = kwargs.get('instance')
    comproba = ComprobanteVenta.objects.get(id=linea.comprobante.id)
    comproba.total = comproba.eldetalle.aggregate(
        total=Sum(F('subtotal')))['total']
    comproba.save()
'''
@receiver(post_save, sender=DetalleVenta)
def trigger_sumadevale(sender, **kwargs):
    linea = kwargs.get('instance')
    fact = ComprobanteVenta.objects.get(id=linea.comprobante.id)
    fact.total = fact.eldetalle.aggregate(total=Sum(F('subtotal')))['total']
    fact.save()
'''
