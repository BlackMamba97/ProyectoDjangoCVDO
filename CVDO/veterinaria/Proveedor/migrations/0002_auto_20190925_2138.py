# Generated by Django 2.2.4 on 2019-09-26 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proveedor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.CharField(max_length=15, verbose_name='Telefono'),
        ),
    ]