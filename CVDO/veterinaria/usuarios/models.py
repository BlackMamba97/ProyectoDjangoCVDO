from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
# Create your models here.


class Empleado(models.Model):
    image = models.ImageField('Ingrese Foto', null=True, blank=True)
    Empleado = models.OneToOneField(User, on_delete=models.CASCADE)
    Sueldo = models.PositiveIntegerField('Sueldo', null=False, blank=False)
    comision = models.FloatField('Comision', null=False, blank=False)

    def image_img(self):
        if self.image:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=self.image.url, width=100, height=100))
        else:
            return 'No existe imagen'
    image_img.short_description = 'Imagen'

    def __str__(self):
        return "%s " % (self.Empleado)

    class Meta:
        db_table = 'Empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
