# Generated by Django 2.2.4 on 2019-09-26 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_auto_20190920_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleventa',
            name='comis',
            field=models.PositiveIntegerField(default=0, verbose_name='Comision'),
        ),
    ]
