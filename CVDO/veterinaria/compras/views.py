from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from .models import *
from usuarios.models import Empleado
from django.shortcuts import redirect

# Create your views here.


class Comprobantecompraview(PDFTemplateView):
    # se crea la clase para crear el informe de compras
    template_name = "comprobantecompra.html"

    def get_context_data(self, **kwargs):
        # se crea el metodo de get_context
        ids = self.request.GET.get("id")
        comprobante = Comprobante.objects.get(id=ids)
        # se crea la vaiable comprobante el
        # cual recupera todos los comprobantes
        detalle = detalle_compra.objects.filter(comprobante=comprobante.id)
        # se crea la variable detalle para
        # capturar todos los detalles de compras
        return super(Comprobantecompraview, self).get_context_data(
            pagesize="Letter",
            title="Comprobantes de Compra",
            # se manda al informe de compras las variables
            # comprobante y detalle
            comprobante=comprobante,
            detalle=detalle,
            **kwargs
            )
