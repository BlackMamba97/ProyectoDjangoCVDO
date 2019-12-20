from django.contrib import admin
from . models import *
# Register your models here.


class CajaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ganancia', 'perdida', 'total']


admin.site.register(Cajas, CajaAdmin)
