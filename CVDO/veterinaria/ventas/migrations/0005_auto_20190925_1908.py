# Generated by Django 2.2.4 on 2019-09-26 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0004_detalleventa_comis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleventa',
            name='comis',
            field=models.FloatField(default=0, verbose_name='Comision'),
        ),
    ]