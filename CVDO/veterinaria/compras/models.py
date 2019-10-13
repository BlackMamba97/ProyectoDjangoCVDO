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


class tipo_pago(models.Model):
    # se crea la clase tipo_pago
    pago = models.CharField('Pago', max_length=20)

    def __str__(self):
        return "%s" % (self.pago)

    class Meta:
        db_table = 'TipoPago'
        verbose_name = 'Tipo pago Compras'
        verbose_name_plural = 'Tipos de pagos de Compras'


class Comprobante(models.Model):
    # se crea la clase comprobante la cual sera la encargada
    # de administrar todas las compras en el sistema
    fecha = models.DateField('fecha', default=date.today)
    # se activa la acción para ingresar la fecha automaticamente
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, null=True)
    # se crea una foranea para redirigir a la tabla proveedores
    total = models.FloatField('Total', null=True, default=0.00)
    pago = models.ForeignKey(tipo_pago, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "%s" % (self.proveedor)

    def save(self, *args, **kwargs):
        super(Comprobante, self).save(*args, **kwargs)

    def compro(self):
        # se crea un metodo para generar el informe de la compra
        # al momento de presionar la imagen de la impresora
        return mark_safe(
            u'<center><a href="/comprobantecompra/?id=%s" target="_blank"><img src="/media/programa/impresora.png"/></a></center>' % self.id)
    compro.short_description = 'Comprobante de Compra'

    class Meta:
        db_table = 'ComprobanteCompra'
        verbose_name = 'Comprobante de Compra'
        verbose_name_plural = 'Comprobantes de Compras'


class detalle_compra(models.Model):
    # se crea el detalle de la compra
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

    def clean(self):
        # se crea metodo clean el cual se detonará antes de guardar
        if not self.pk:
            # si no existe una pk que representa si existe un
            # detalle
            isnew = True
            # la variable isnew se vuelve True
        else:
            # si no
            isnew = False
            # la variable isnew se vuelve False

        with transaction.atomic():
            if isnew:
                deta = DetalleProducto.objects.filter(producto=self.producto)
                # se crea deta que almacena todos los detalles
                # de productos filtrandolos por producto
                for delta in deta:
                    # se crea un ciclo que recorra el detalle
                    # de todos los productos
                    if self.fechavencimiento is None:
                        # si no existe fechavencimiento
                        # en el producto ingresado
                        ()
                    else:
                        # si no
                        if self.numeroloteproducto is None:
                            # verifique si exista numero de lote
                            # en el producto ingresado
                            raise ValidationError(
                                'El producto debe tener un numero de lote asignado')
                            # retorna la leyenda El producto
                            # debe tener un num de lote
                        else:
                            ()
                            # no hace nada

    def save(self, force_insert=False, force_update=False, using=None):
        # se crea el metodo save el cual detonará las acciones despues
        # de apachar el boton grabar
        self.subtotal = self.cantidad * self.preciocompra
        # define que el subtotal sera igual a la cantida dy el precio de compra
        if not self.pk:
            isnew = True
        else:
            isnew = False

        with transaction.atomic():
            if isnew:
                if self.fechavencimiento is None:
                    # si la fechavencimiento es nulo
                    targe = DetalleProducto.objects.filter(
                        producto=self.producto).last()
                    if targe is None:
                        # si no existe un detalle de producto
                        target = DetalleProducto()
                        target.producto = self.producto
                        target.cantidad = self.cantidad
                        target.FechaCompra = self.FechaCompra
                        target.preciocompra = self.preciocompra
                        target.precioventa = self.precioventa
                        target.numeroloteproducto = self.numeroloteproducto
                        # se ingresan todos los datos y se guarda en detalle
                        # de producto automaticamente

                        target.ubicacion = self.ubicacion
                        # Se guarda el detalle de Producto
                        target.save()
                    else:
                        if self.preciocompra == targe.preciocompra and self.precioventa == targe.precioventa:
                            # si el precio de compra es igual a algun preciocompra y precioventa
                            # es igual a algun precio venta
                            # unicamente actualiza la cantidad del detalle
                            targe.cantidad = targe.cantidad + self.cantidad
                            # se graba el detalle del producto
                            targe.save()
                        else:
                            # si no se parecen los precios
                            # ingresa todos los datos
                            target = DetalleProducto()
                            target.producto = self.producto
                            target.cantidad = self.cantidad
                            target.FechaCompra = self.FechaCompra
                            target.preciocompra = self.preciocompra
                            target.precioventa = self.precioventa
                            target.numeroloteproducto = self.numeroloteproducto
                            target.ubicacion = self.ubicacion
                            # target.estado = True
                            target.save()
                            # se graba el detalle del producto
                else:
                    if self.numeroloteproducto is None:
                        ()
                    else:
                        # si existe numero de lote del producto
                        target = DetalleProducto()
                        target.producto = self.producto
                        target.FechaCompra = self.FechaCompra
                        target.cantidad = self.cantidad
                        target.numeroloteproducto = self.numeroloteproducto
                        target.preciocompra = self.preciocompra
                        target.precioventa = self.precioventa
                        target.fechavencimiento = self.fechavencimiento
                        target.ubicacion = self.ubicacion
                        # se ingresan los atributos
                        # y se guardan los datos del detalle
                        target.save()
            else:
                ()
            super(detalle_compra, self).save(force_insert, force_update, using)

# ------------------------------Metodo para ingresar a otro detalle---------------------------

    def eliminar(self):
        # se crea el metodo eliminar
        detalle = DetalleProducto.objects.all()
        for i in detalle:
            if (
                i.FechaCompra==self.FechaCompra and i.preciocompra==self.preciocompra and i.precioventa==self.precioventa or i.numeroloteproducto==self.numeroloteproducto and i.preciocompra==self.preciocompra and i.precioventa==self.precioventa):
                    detalle = i
                    # Si los datos de fecha compra,preciocompra y precio venta
                    # son iguales solo cambia la variable cantidad y
                    # resta las existencias
                    detalle.cantidad = detalle.cantidad - self.cantidad
                    # y se guarda el detalle del producto
        detalle.save()

    def delete(self, *args, **kwargs):
        # se define el metodo delete
        # y se manda a llamar el metodo eliminar
        self.eliminar()
        super(detalle_compra, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'DetalleCompra'
        verbose_name = 'detalle compra'
        verbose_name_plural = 'detalle de compras'


@receiver(post_save, sender=detalle_compra)
def trigger_sumadevale(sender, **kwargs):
    # se crea un trigger el cual sumara todos los subtotales de
    # las compras y se sumaran al total de comprobante
    linea = kwargs.get('instance')
    fact = Comprobante.objects.get(id=linea.comprobante.id)
    fact.total = fact.Eldetalle.aggregate(total=Sum(F('subtotal')))['total']
    fact.save()
