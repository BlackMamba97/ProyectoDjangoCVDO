# Generated by Django 2.1.7 on 2019-10-03 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0010_auto_20191002_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleproducto',
            name='estado',
            field=models.BooleanField(blank=True, editable=False, null=True, verbose_name='Estado'),
        ),
    ]