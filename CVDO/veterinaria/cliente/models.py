from django.db import models

# Create your models here.


class Cliente(models.Model):
    NIT = models.CharField(
        'Ingrese NIT', max_length=9, null=False, primary_key=True, unique=True)
    nombre = models.CharField('Nombre', max_length=50)
    apellido = models.CharField('Apellido', max_length=50)
    direccion = models.CharField('Direccion', max_length=50)
    telefono = models.CharField('Telefono', max_length=15)

    def __str__(self):
        return "%s %s" % (
            self.nombre, self.apellido)

    class Meta:
        db_table = 'Cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
