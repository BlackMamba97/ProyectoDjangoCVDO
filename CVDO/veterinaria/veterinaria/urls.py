"""veterinaria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from ventas.views import Comprobanteview, FichadeVentas, FichadeVentashoy, FichadeVentasmes, FichadeVentasaño
from compras.views import Comprobantecompraview
from productos.views import FichadeProductos, FichadeProductosproximos, FichadeProductosOrden
from productos.views import FichadeProductos2, FichadeProductosproximos2, FichadeProductosOrden2

urlpatterns = [
    path('veterinaria/', admin.site.urls),
    # path('chaining/', include('smart_selects.urls')),
    url(r"^comprobanteventa/(?P<id>)", Comprobanteview.as_view()),
    url(r"^comprobantecompra/(?P<id>)", Comprobantecompraview.as_view()),
    url(r"^InformeVentas/", FichadeVentas.as_view()),
    url(r"^InformedeProductosVencidos/", FichadeProductos.as_view(
        ), name="informevencido"),
    url(r"^InformedeProductosdeOfertas/", FichadeProductosproximos.as_view(
        ), name="informeoferta"),
    url(r"^InformedeProductosenOrden/", FichadeProductosOrden.as_view(
        ), name="informeorden"),
    # ---------------------------
    url(r"^InformedeProductosVencidos2/", FichadeProductos2.as_view(
        ), name="informevencido2"),
    url(r"^InformedeProductosdeOfertas2/", FichadeProductosproximos2.as_view(
        ), name="informeoferta2"),
    url(r"^InformedeProductosenOrden2/", FichadeProductosOrden2.as_view(
        ), name="informeorden2"),
    # --------Ventas de HOY, MES, AÑO--
    url(r"^comprobanteventahoy/", FichadeVentashoy.as_view(
        ), name="ventasdia"),
    url(r"^comprobanteventames/", FichadeVentasmes.as_view(
        ), name="ventasmes"),
    url(r"^comprobanteventasaño/", FichadeVentasaño.as_view(
        ), name="ventasanual"),
    url(r"^comprobanteventa/(?P<id>)", Comprobanteview.as_view()),
    ]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
