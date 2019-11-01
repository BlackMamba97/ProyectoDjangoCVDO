from django.db import models
from cliente.models import Cliente
from productos.models import Producto, DetalleProducto, Productos_Empleado
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models import Sum, F
from django.db.models.signals import post_save
from usuarios.models import Empleado
from datetime import date


class TipoPago(models.Model):
    # se crea la clase Tipopago
    Pago = models.CharField('Tipo de Pago', max_length=30)

    def __str__(self):
        return "%s" % (self.Pago)


class ComprobanteVenta(models.Model):
    # Se crea la clase padre llamada ComprobanteVenta
    fecha = models.DateField('Fecha de Venta', default=date.today)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=False)
    total = models.FloatField('Total', null=True, default=0.00)
    pago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, null=False)
    efectivo = models.FloatField('Efectivo', null=True, default=0.00)
    vuelto = models.FloatField('Vuelto', null=True, default=0.00)
    # se crea el atributo vendedor el cual será encargado
    # de retornar el nombre de usuario que tiene la sesión
    # abierta en el sistema
    vendedor = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "%s %s" % (self.fecha, self.cliente)

    # def comisi(self):
    #    ven = Empleado.objects.filter(Empleado=self.vendedor)
    #        ven.comision = ven.comision + ()

    def save(self, *args, **kwargs):
        # se crea metodo save para el cual selecciona el
        # atributo vuelto y genera la accion agregandole que
        # será igual al efectivo menos el total
        self.vuelto = self.efectivo - self.total
        super(ComprobanteVenta, self).save(*args, **kwargs)

    def compro(self):
        # generando metodo para que muestr una imagen de impresora
        # al momento de querer generar el comprobante de venta
        return mark_safe(
            u'<center><a href="/comprobanteventa/?id=%s" target="_blank"><img src="/media/programa/impresora.png"/></a></center>' % self.id)
    compro.short_description = 'Comprobante de Venta'

    class Meta:
        db_table = 'ComprobanteVenta'
        verbose_name = 'Comprobante de Venta'
        verbose_name_plural = 'Comprobante de Ventas'


class DetalleVenta(models.Model):
    # se crea la segunda clase mas importante
    # ya que en ella consta todos los detalles
    # que se generan en las ventas
    comprobante = models.ForeignKey(
        ComprobanteVenta, on_delete=models.CASCADE, null=True, blank=True,
        related_name='eldetalle')
    producto = models.ForeignKey(
        Productos_Empleado, on_delete=models.CASCADE, null=True)
    numeroloteproducto = models.CharField(
       'Numero de lote',
       max_length=20, null=True, blank=True)
    cantidad = models.PositiveIntegerField('Cantidad', default=0)
    # se crea atributo comis el cual consiste en
    # proporcionar comision al vendedor en caso
    # el articulo tenga porcenje de comision
    comis = models.FloatField('Comision', default=0)
    subtotal = models.FloatField(
        'subtotal', null=False, blank=False, default=0)

    def preciov(self):
        # se crea accion para definir que la variable precio
        # sera igual a subtotal dividido la cantidad de producto
        precio = self.subtotal/self.cantidad
        # retornando así el precio
        return precio

    def clean(self):
        if not self.pk:
            isnew = True
        else:
            isnew = False

        with transaction.atomic():
            if isnew:
                # se crea la accion de Clean el cual
                # validará toda la información antes de
                # guardar la información
                prode = DetalleProducto.objects.filter(
                        producto=self.producto).first()
                det = DetalleProducto.objects.filter(
                    producto=self.producto).all()
                pro = Producto.objects.filter(
                                nombre=self.producto.nombre).get()
                if prode.fechavencimiento is None:
                    # si el producto ingresado en pantalla no tiene
                    # fecha de vencimiento entonces
                    # se genera un ciclo que recorre todos los
                    # detalles de productos
                    for i in det:
                        detonador = i
                        if detonador.numeroloteproducto == self.numeroloteproducto:
                            # si el numerolote de  lavariable del ciclo
                            # es igual a la que se acaba de ingresar entonces
                            if detonador.cantidad > 0:
                                # verifique que la cantidad de ese
                                # producto sea mayor a 0
                                # si es así
                                if self.cantidad > pro.existencia:
                                    # verifique que la cantidad ingresada sea mayor a
                                    # la cantidad de existencias con las que cuenta el
                                    # producto
                                    raise ValidationError(
                                        # retorna que no hay existencias
                                        # para realizar esa venta
                                        ' No tenemos en existencia{}'.format(
                                            self.cantidad) +
                                        ' solo contamos con {}'.format(
                                            pro.existencia))
                                else:
                                    # si la cantidad es menor que las existencias
                                    if detonador.cantidad >= self.cantidad:
                                        # verifica si la cantidad de el producto
                                        # con ese numero de lote es mayor o igual
                                        # se realiza la venta
                                        ()
                                    else:
                                        # si la cantidad del detalle es menor
                                        # retorna una alerta
                                        # de verificación
                                        raise ValidationError(
                                            ' Verifique las existencias ya que varían los precios de {}'.format(
                                                de.producto))
                            else:
                                # si la cantidad del producto es 0
                                # no se puede vender ningun producto
                                # porque no se cuenta con existencias
                                ()
                        else:
                            # si no existe ningun producto con el mismo numero de lote
                            # retorna la leyenda el numero de lote ingresado no existe
                            raise ValidationError(
                                'El numero de lote ingresado no existe')
                else:

                    if self.cantidad > pro.existencia:
                                    # verifique que la cantidad ingresada sea mayor a
                                    # la cantidad de existencias con las que cuenta el
                                    # producto
                                    raise ValidationError(
                                        # retorna que no hay existencias
                                        # para realizar esa venta
                                        ' No tenemos en existencia{}'.format(
                                            self.cantidad) +
                                        ' solo contamos con {}'.format(
                                            pro.existencia))
                        # si el articulo a venter no tiene fecha vencimiento
                    else:
                        if self.numeroloteproducto is None:
                            # verifica si no cuenta con numero de lote
                            # si es así genera una alerta
                                    raise ValidationError(
                                        ' Este Producto necesita ingresar Numero de Lote para ser vendido')
                        else:
                            # si cuenta con numero de lote
                            try:
                                prod = DetalleProducto.objects.filter(
                                    numeroloteproducto=self.numeroloteproducto).filter(
                                    producto=self.producto).get()
                                    # se crea una variable que obtenga los detalles de
                                    # producto filtrandolos por nombre
                            except DetalleProducto.DoesNotExist:
                                # se genera una excepción xq no encuentra el numero de lote
                                raise ValidationError(
                                            'El numero de lote no existe')
                            pro = Producto.objects.filter(
                                nombre=self.producto.nombre).get()
                            # se crea variable pro para obtener los productos
                            # con el mismo nombre que el nombre que se ingreso
                            if prod.fechavencimiento > date.today():
                                # se genera una condición si la fecha vencimiento es
                                # mayor a el dia actual
                                if pro.existencia >= self.cantidad:
                                    # verifique si hay mas existencias de las que
                                    # se solicitan en la venta
                                    if prod.cantidad >= self.cantidad:
                                        # verifica si el producto con ese numero de lote
                                        # cuenta con la cantidad que se solicita en la venta
                                        ()
                                    else:
                                        # si no hay suficiente cantidad de producto
                                        # con ese numero de lote genera una alerta
                                        raise ValidationError(
                                            'Este numero de lote solo cuenta con {}'.format(
                                                prod.cantidad) + ' unidades')
                                else:
                                    # si no hay existencias se genera una alerta
                                    raise ValidationError(
                                        ' No tenemos en existencia {}'.format(
                                            self.cantidad) +
                                        ' solo contamos con {}'.format(
                                            pro.existencia))
                            else:
                                # si el articulo esta vencido genera una alerta que indica
                                # que el articulo esta vencido
                                raise ValidationError(
                                        ' El producto con número de Lote {}'.format(
                                            self.numeroloteproducto) +
                                        ' vencía en la fecha {}'.format(
                                            prod.fechavencimiento))

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
                            detonador = i
                            if detonador.numeroloteproducto == self.numeroloteproducto:
                                if detonador.cantidad > 0:
                                    if self.cantidad > pro.existencia:
                                        ()
                                    else:
                                        if detonador.cantidad >= self.cantidad:
                                            detonador.cantidad = (
                                                detonador.cantidad - self.cantidad)
                                            self.subtotal = (
                                                self.cantidad * detonador.precioventa)
                                            self.comis = (
                                                self.cantidad * detonador.precioventa * (
                                                    pro.porcentaje/100))
                                            emp = Empleado.objects.filter(
                                                Empleado=self.comprobante.vendedor.id).get()
                                            print('---------------')
                                            print(emp.comision)
                                            print(emp)
                                            emp.comision = emp.comision + self.comis
                                            emp.save()
                                            detonador.save()
                                        else:
                                            ()
                                else:
                                    ()
                            else:
                                ()
                else:

                    if self.numeroloteproducto is None:
                        ()
                    else:
                        try:
                            prod = DetalleProducto.objects.filter(
                                numeroloteproducto=self.numeroloteproducto).filter(
                                producto=self.producto).get()
                        except DetalleProducto.DoesNotExist:
                            raise ValidationError(
                                'El numero de lote no existe')
                        if self.numeroloteproducto == prod.numeroloteproducto:
                            # produc = DetalleProducto.objects.filter(
                            #     estadoo='Producto en Orden').get()
                            pro = Producto.objects.filter(
                                nombre=self.producto.nombre).get()
                            hoy = date.today()
                            # print(produc.estadoo)
                            print('-----------------------------------------------')
                            if prod.fechavencimiento > hoy:
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

        super(DetalleVenta, self).save(force_insert, force_update, using)

    def eliminar(self):
        detpro = DetalleProducto.objects.all()
        for i in detpro:
            preci = self.subtotal/self.cantidad
            if (
                i.numeroloteproducto==self.numeroloteproducto  and i.precioventa==preci or i.precioventa==preci):
                    detpro = i
                    self.comprobante.total = (
                        self.comprobante.total - self.subtotal)
                    detpro.cantidad = detpro.cantidad + self.cantidad
                    emp = Empleado.objects.filter(
                        Empleado=self.comprobante.vendedor.id).get()
                    emp.comision = emp.comision - self.comis
                    self.comprobante.save()
                    emp.save()
                    detpro.save()

    def delete(self, *args, **kwargs):
        self.eliminar()
        super(DetalleVenta, self).delete(*args, **kwargs)

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
