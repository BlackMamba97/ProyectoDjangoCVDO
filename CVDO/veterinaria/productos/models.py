from django.db import models
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum, F
from django.utils.html import format_html
from datetime import date
from datetime import datetime
from django.utils import timezone
# Create your models here.


# creación de modelo de Tipo de Producto(categoria)
class tipoproducto(models.Model):
    TipoProducto = models.CharField(
        'Tipo de Producto', max_length=150)

    def __str__(self):
        return "%s " % (self.TipoProducto)

    class Meta:
        db_table = 'tipoproducto'
        verbose_name = 'tipoproducto'
        verbose_name_plural = 'tipoproductos'


# creación de modelo Producto con todos los atributos correspondientes
class Producto(models.Model):
    image = models.ImageField('Ingrese Imagen', null=True, blank=True)
    nombre = models.CharField('Nombre', max_length=150)
# inserción de tipo producto que sera una llave foranea de tipoproducto
    tipoProducto = models.ForeignKey(
        tipoproducto, on_delete=models.CASCADE, null=True, blank=True)
    porcentaje = models.PositiveIntegerField(
        'Porcentaje', blank=True, null=True, default=0)
    meses = models.PositiveIntegerField(
        'Meses a Vencerse', null=True, blank=True)
    existencia = models.PositiveIntegerField(
        'existencia', default=0)

# creación de metodo para guardar una imagen
    def image_img(self):
        if self.image:
            # retorna un mrk_safe el cual es el import que permite
            # visualizar la imagen en el modelo
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=self.image.url, width=50, height=50))
        else:
            # si no se ingresa imagen se retornará No existe imagen
            return 'No existe imagen'
    image_img.short_description = 'Imagen'

    # el atributo que retornará el producto
    def __str__(self):
        return "%s " % (self.nombre)

    # creacion de metodo para mostrar las existencias
    def Pro(self):
        # si las existencias del producto son menores o iguales a 10 el numero
        # será de color rojo
        if self.existencia <= 10:
            return format_html(
                '<p style="color: #FF0000;">' + str(self.existencia) + '</p>'
                )
        else:
            # Sino sera de color azul
            return format_html(
                '<p style="color: #2874A6;">' + str(self.existencia) + '</p>'
                )
    Pro.short_description = 'Existencias'

    class Meta:
        db_table = 'Producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Productos_Empleado(Producto):
    # definición de Productos para los empleados
    # el cual no tendrá acceso al precio costo
    def __str__(self):
        return "%s " % (self.nombre)

    class Meta:
        proxy = True
# Productos_Empleado.short_description = 'Productos Empleados'


class ubicacion(models.Model):
    # creación de modelo ubicación el cual estará en el
    # detalle de producto
    ubicacionproducto = models.CharField(
        'Ubicacion del Producto',
        max_length=150, null=True)

    def __str__(self):
        return "%s " % (self.ubicacionproducto)

    class Meta:
        db_table = 'Ubicacion'
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'


class DetalleProducto(models.Model):
    # creación de modelo Detalle Producto
    # el cual contara con varios atributos y foraneas
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, null=False, blank=False,
        related_name='elproducto')
    numeroloteproducto = models.CharField(
        'Numero de lote del Producto',
        max_length=50, null=True, blank=True)
    FechaCompra = models.DateField(
        'FechaCompra')
    cantidad = models.PositiveIntegerField(
        'Cantidad', null=True, default=0)
    preciocompra = models.FloatField(
        'Precio Costo', null=False, blank=False, default=0)
    precioventa = models.FloatField(
        'Precio Venta', null=False, blank=False, default=0)
    fechavencimiento = models.DateField(
        'Fecha de Vencimiento', null=True, blank=True)
    ubicacion = models.ForeignKey(
        ubicacion, on_delete=models.CASCADE, null=True, blank=True)

    def estadoo(self):
        # creación de metodo estadoo para determinar
        # si el producto esta vencido
        # graba en variable today la fecha exacta del dia de hoy
        today = date.today()
        # la variable year sera la diferencia entre el año de la
        # fecha vencimietno con el año en el que estamos
        year = (self.fechavencimiento.year - today.year)
        # month muestra la diferencia entre el mes en el que estamos
        # con el mes de fecha vencimiento
        month = (self.fechavencimiento.month - today.month)
        # day muestra  la diferencia entre los dias de
        # la fecha vencimiento con la fecha actual
        day = (self.fechavencimiento.day - today.day)
        daypro = (self.fechavencimiento)
        totalyear = (year * 12)
        meses = (month + totalyear)
        fecha = month + totalyear
        pro = Producto.objects.all()
        # la variable pro trae todos los productos que existen
        # Se genera un ciclo que recorra todos los productos
        for i in pro:
            pro = i
            if(pro == self.producto):
                # si el producto del ciclo es igual al producto ingresado
                if pro.meses is not None:
                    # verifique el atributo meses de la tabla producto
                    # no este vacio
                        #pro = i
                    # fecha 2 será igual a la cantidad de meses
                    fecha2 = int(pro.meses)
                    if(self.cantidad <= 0):
                        # si el atributo cantidad es menor o igual a 0
                        return format_html(
                            '<center> <p style="color: #B40404;">'
                            'Sin existencia </p></center>'
                            )
                    elif(meses < 1 and day < 1):
                        # si la variable meses es menor a uno y la variable day
                        # es menor que uno retorne producto vencido
                        return format_html(
                            '<center> <p style="color: #B40404;">Producto Vencido</p> </center>'
                            )
                    elif (meses > fecha2):
                        # si la variable meses es mayor que fecha 2
                        # que imprima en pantalla Producto en Orden
                        return format_html(
                            '<center> <p style="color: #0404B4;">Producto en Orden</p></center>'
                            )
                    elif(self.fechavencimiento <= today):
                        # Sino que retorne producto vencido
                        return format_html(
                                '<center> <p style="color: #B40404;">Producto Vencido</p> </center>'
                                )
                    elif(meses <= fecha2):
                        # si variable meses es menor o igual que fecha 2
                        # que imprima en pantalla Producto se debe Ofertar
                        return format_html(
                            '<center> <p style="color: #FF4000;">Producto se debe Ofertar</p> </center>'
                            )
            else:
                    ()
        pro.save()
    estadoo.short_description = 'Estado de Producto'

    def fechaq(self):
        # creación de metodo para capturar los días
        # restantes para el producto antes de vencerse
        today = date.today()
        # graba en variable today la fecha exacta del dia de hoy
        year = (self.fechavencimiento.year - today.year)
        # la variable year sera la diferencia entre el año de la
        # fecha vencimietno con el año en el que estamos
        month = (self.fechavencimiento.month - today.month)
        # month muestra la diferencia entre el mes en el que estamos
        # con el mes de fecha vencimiento
        day = (self.fechavencimiento.day - today.day)
        # day muestra  la diferencia entre los dias de
        # la fecha vencimiento con la fecha actual
        totalyear = (year * 12)
        meses = (month + totalyear)
        # si la variable meses es menor o igual a 0
        # y la variable day es menor o igual a 0
        if(meses <= 0 and day <= 0):
            # que imprima producto vencido
            return format_html(
                '<center> <p style="color: #FF0000;">'
                'Producto Vencido</p></center>'
                )
        elif(self.fechavencimiento < today):
            return format_html(
                '<center> <p style="color: #FF0000;">'
                'Producto Vencido</p></center>'
                )
        elif(meses > 1):
            # sino verifique si meses es mayor a 1
            return (str(month + totalyear) + (' Meses '))
            # que retorne la fecha en meses
        elif(meses == 1):
            # sino verifique si meses es igual a 1
            meses = meses*30
            return (str(day + meses) + (' días '))
            # que retorne la fecha en dias
        elif(meses <= 0):
            # sino verifique que meses es menor o igual a 0
            return (str(day + meses) + (' días '))
            # que retorne la fecha en dias
        elif(day <= 0):
            # sino verifique si day es menor o igual a 0
            return format_html(
                '<center> <p style="color: #FF0000;">'
                'Producto Vencido</p></center>'
                )
            # que retorne Producto Vencido
    fechaq.short_description = 'Fecha a Vencer'

    def validador(self):
        # generador de variable para impresion en el informe
        today = date.today()
        year = (self.fechavencimiento.year - today.year)
        month = (self.fechavencimiento.month - today.month)
        day = (self.fechavencimiento.day - today.day)
        totalyear = (year * 12)
        meses = (month + totalyear)
        oferta = False
        fecha = month + totalyear
        pro = Producto.objects.all()
        # no = (self.producto)
        for i in pro:
            pro = i
            if(pro == self.producto):
                if pro.meses is not None:
                    fecha2 = int(pro.meses)
                    if(self.cantidad <= 0):
                            pass
                    elif(meses < 1 and day < 1):
                        pass
                    elif (meses > fecha2):
                        pass
                    elif(meses <= fecha2):
                        oferta = True
                        return oferta
                else:
                    pass
            else:
                    ()

    def delete(self, *args, **kwargs):
        self.producto.existencia = self.producto.existencia - self.cantidad
        self.producto.save()
        super(DetalleProducto, self).delete(*args, **kwargs)

    def __str__(self):
        return "%s " % (self.producto.nombre)

    class Meta:
        db_table = 'DetalleProducto'
        verbose_name = 'Detalle de Producto'
        verbose_name_plural = 'Detalle de Productos'


class DetalleProducto_Empleado(DetalleProducto):
    # Generación de Modelo de Detalle de Producto para los vendedores
    def __str__(self):
        return "%s " % (self.producto.nombre)

    class Meta:
        proxy = True


@receiver(post_save, sender=DetalleProducto)
def trigger_suma(sender, **kwargs):
    # creación de trigger para sumar automaticamente todas los
    # existencias con las que cuente un detalle de producto
    linea = kwargs.get('instance')
    su = Producto.objects.get(id=linea.producto.id)
    su.existencia = su.elproducto.aggregate(
        existencia=Sum(F('cantidad')))['existencia']
    su.save()
