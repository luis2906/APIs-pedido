from django.contrib import admin

# Register your models here.
from .models import Estado, Pedido

class EstadoAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'cliente', 'articulo', 'cantidad', 'estado' , 'is_active')

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Pedido, PedidoAdmin)