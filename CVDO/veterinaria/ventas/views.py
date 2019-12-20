from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from .models import *
from usuarios.models import Empleado
from django.shortcuts import redirect


class Comprobanteview(PDFTemplateView):
    template_name = "comprobanteventa.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        comprobante = ComprobanteVenta.objects.get(id=ids)
        detalle = DetalleVenta.objects.filter(comprobante=comprobante.id)
        return super(Comprobanteview, self).get_context_data(
            pagesize="Letter",
            title="Comprobantes de Ventas",
            comprobante=comprobante,
            detalle=detalle,
            **kwargs
            )


class FichadeVentas(PDFTemplateView):
    template_name = "InformedeVentas.html"

    def get_context_data(self, **kwargs):
        prods = ComprobanteVenta.objects.filter()
        return super(FichadeVentas, self).get_context_data(
            pagesize="Letter",
            title="Ventas",
            prods=prods,
            **kwargs
            )

# FICHAS PARA CREAR LAS VENTAS DÍA MES AÑO


class FichadeVentashoy(PDFTemplateView):
    template_name = "InformedeVentashoy.html"

    def get_context_data(self, **kwargs):
        day = date.today()
        prods = ComprobanteVenta.objects.filter(
            fecha=day).extra(order_by=['fecha'])

        return super(FichadeVentashoy, self).get_context_data(
            pagesize="Letter",
            title="Ventas",
            prods=prods,
            day=day,
            **kwargs
            )


class FichadeVentasmes(PDFTemplateView):
    template_name = "InformedeVentasmes.html"

    def get_context_data(self, **kwargs):
        day = date.today()
        prods = ComprobanteVenta.objects.filter(
            ).extra(order_by=['fecha'])
        return super(FichadeVentasmes, self).get_context_data(
            pagesize="Letter",
            title="Ventas",
            prods=prods,
            day=day,
            **kwargs
            )


class FichadeVentasaño(PDFTemplateView):
    template_name = "InformedeVentasaño.html"

    def get_context_data(self, **kwargs):
        day = date.today()
        prods = ComprobanteVenta.objects.filter().extra(order_by=['fecha'])

        return super(FichadeVentasaño, self).get_context_data(
            pagesize="Letter",
            title="Ventas",
            prods=prods,
            day=day,
            **kwargs
            )

# Create your views here.
