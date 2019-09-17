from django.contrib import admin
from .models import Empleado
# Register your models here.


class Empleado_Admin(admin.ModelAdmin):
    list_display = ['image_img', 'Empleado', 'Sueldo']
    list_filter = ['Empleado', 'Sueldo']

admin.site.register(Empleado, Empleado_Admin)
