# Generated by Django 2.2.4 on 2019-08-28 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_auto_20190826_2204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detalle_compra',
            options={'verbose_name': 'detalle compra', 'verbose_name_plural': 'detalle de compras'},
        ),
    ]