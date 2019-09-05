from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
# Create your models here.


class Empleado(models.Model):
    image = models.ImageField('Ingrese Foto', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Sueldo = models.PositiveIntegerField('Sueldo', null=True, blank=True)
    comision = models.PositiveIntegerField('Comision', null=True, blank=True)

    def image_img(self):
        if self.image:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=self.image.url, width=100, height=100))
        else:
            return 'No existe imagen'
    image_img.short_description = 'Imagen'

    def __str__(self):
        return "%s " % (self.user)

    class Meta:
        db_table = 'Empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
