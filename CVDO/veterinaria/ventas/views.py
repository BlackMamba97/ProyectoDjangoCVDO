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

# Create your views here.
