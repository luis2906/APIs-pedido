from django.contrib import admin

# Register your models here.
from .models import Estado, Pedido, PedidoArticulo

class EstadoAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'cliente', 'estado' , 'is_active')

class PedidoArticuloAdmin(admin.ModelAdmin):
	list_display = ('id', 'pedido', 'articulo', 'cantidad', 'is_active')

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PedidoArticulo, PedidoArticuloAdmin)
