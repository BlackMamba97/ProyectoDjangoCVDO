from django.db import models

# Create your models here.


class Cajas(models.Model):
    nombre = models.CharField('Nombre', max_length=150)
    perdida = models.FloatField('Perdidas', null=True, default=0.00)
    ganancia = models.FloatField('Ganancias', null=True, default=0.00)
    total = models.FloatField('Total', null=True, default=0.00)

    def __str__(self):
        return "%s %s" % (self.ganancia, self.perdida)

    def save(self, *args, **kwargs):
        # se crea metodo save para el cual selecciona el
        # atributo vuelto y genera la accion agregandole que
        # será igual al efectivo menos el total
        self.total = self.ganancia - self.perdida
        super(Cajas, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Cajas'
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'
