"""ujueta URL Configuration

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
from django.urls import path
from django.conf.urls import  include, url
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from django.conf.urls.static import static

admin.autodiscover()
# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()

# articulos.views
from articulos.views import ArticuloViewSet, MarcaViewSet 
router.register(r'articulos', ArticuloViewSet)
router.register(r'marcas', MarcaViewSet)
# clientes.views
from clientes.views import ClienteViewSet 
router.register(r'clientes', ClienteViewSet)
# pedidos.views
from pedidos.views import PedidoViewSet,EstadoViewSet,PedidoArticuloViewSet 
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedido-articulos', PedidoArticuloViewSet)
router.register(r'estados', EstadoViewSet)


urlpatterns = [
     path('admin/', admin.site.urls),
    url(r'^api/',include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
