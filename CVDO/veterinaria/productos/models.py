from django.db import models
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum, F
from django.utils.html import format_html
from datetime import date
from datetime import datetime
# Create your models here.


class Producto(models.Model):
    image = models.ImageField('Ingrese Imagen', null=True, blank=True)
    nombre = models.CharField('Nombre', max_length=150)
    porcentaje = models.PositiveIntegerField(
        'Porcentaje', blank=True, null=True)
    meses = models.PositiveIntegerField(
        'Meses a Vencerse', null=True, blank=True, default=1)
    existencia = models.PositiveIntegerField(
        'existencia', default=0)

    def image_img(self):
        if self.image:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=self.image.url, width=100, height=100))
        else:
            return 'No existe imagen'
    image_img.short_description = 'Imagen'

    def __str__(self):
        return "%s " % (self.nombre)

    def Pro(self):
        if self.existencia <= 10:
            return format_html(
                '<center><h1 style="color: #FF0000;">' + str(self.existencia) + '</h1></center>'
                )
        else:
            return format_html(
                '<center><h1 style="color: #D7DF01;">' + str(self.existencia) + '</h1></center>'
                )
    Pro.short_description = 'Existencias'

    class Meta:
        db_table = 'Producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class ubicacion(models.Model):
    ubicacionproducto = models.CharField(
        'Ubicacion del Producto',
        max_length=150, null=True, default='Estante 1')

    def __str__(self):
        return "%s " % (self.ubicacionproducto)

    class Meta:
        db_table = 'Ubicacion'
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'


class DetalleProducto(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, null=False, blank=False,
        related_name='elproducto')
    numeroloteproducto = models.CharField(
        'Numero de lote del Producto',
        max_length=150, null=False)
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
    # estado = models.BooleanField('Estado de Producto', default=True)

    def estadoo(self):
        today = date.today()
        # print('hola')
        year = (self.fechavencimiento.year - today.year)
        # print('aqui ya no', year)
        month = (self.fechavencimiento.month - today.month)
        # print('y aqui__', month)
        day = (self.fechavencimiento.day - today.day)
        totalyear = (year * 12)
        meses = (month + totalyear)
        fecha = month + totalyear
        pro = Producto.objects.all()
        print('entra??????')
        # no = (self.producto)
        print(pro)
        for i in pro:
            pro = i
            if(pro == self.producto):
                print('nombre como estamos')
                    #pro = i
                fecha2 = int(pro.meses)
                print(fecha)
                print(pro.meses)
                if(meses < 1 and day < 1):
                    return format_html(
                        '<center> <p style="color: #FF0000;"> Producto Vencido </p> </center>'
                        )
                        # target.estado = False
                elif (meses > fecha2):
                    return format_html(
                        '<center> <p style="color: #0404B4;"> Producto en Orden </p></center>'
                        )
                elif(meses <= fecha2):
                    return format_html(
                        '<center> <p style="color: #FF8000;"> Producto a ofertar </p> </center>'
                        )
            else:
                    print('son diferentes')
        pro.save()
            # target.estado = True
    estadoo.short_description = 'Estado de Producto'
    # -------------------------------------
    # def fechaq(self):
    # today = date.today()
    #    fech1 = datetime.datetime.strptime(str(
    #        self.fechavencimiento), '%Y-%m-%d')
    #    fech2 = datetime.datetime.strptime(
    #        str(today), '%Y-%m-%d')
    #    fech = fech1 - fech2
    #    return (fech)
    # fechaq.short_description = 'Meses a Vencerse'
    # --------------------------------------------

    def fechaq(self):
        today = date.today()
        # print('hola')
        year = (self.fechavencimiento.year - today.year)
        # print('aqui ya no', year)
        month = (self.fechavencimiento.month - today.month)
        # print('y aqui__', month)
        day = (self.fechavencimiento.day - today.day)
        totalyear = (year * 12)
        meses = (month + totalyear)
        if(meses < 1 and day < 1):
            return format_html(
                '<center> <p style="color: #FF0000;">'
                'Producto Vencido </p></center>'
                )
        elif(meses == 1):
            meses = meses*30
            return (str(day + meses) + (' días '))
        else:
            return (str(month + totalyear) + (' Meses '))
    fechaq.short_description = 'Meses a Vencerse'

        # super(DetalleProducto, self).clean()
        # fe = self.fechaq
        # pro = Producto.objects.filter(Producto=self.producto)
        # if(fe <= pro.meses):
        #    self.estado = False
        # else:
        #    self.estado = True

    def __str__(self):
        return "%s " % (self.producto.nombre)

    class Meta:
        db_table = 'DetalleProducto'
        verbose_name = 'Detalle de Producto'
        verbose_name_plural = 'Detalle de Productos'


@receiver(post_save, sender=DetalleProducto)
def trigger_suma(sender, **kwargs):
    linea = kwargs.get('instance')
    su = Producto.objects.get(id=linea.producto.id)
    su.existencia = su.elproducto.aggregate(
        existencia=Sum(F('cantidad')))['existencia']
    su.save()
