from django.db import models

from articulos.models import Articulo
from clientes.models import Cliente
# Create your models here.

class Estado(models.Model):
	nombre = models.CharField(unique=True, max_length=255)

	def __str__(self):
		return self.nombre 
	
class Pedido(models.Model):

	cliente = models.ForeignKey(Cliente, related_name="Pedido_cliente", on_delete=models.PROTECT)
	estado = models.ForeignKey(Estado, related_name="Pedido_estado", on_delete=models.PROTECT)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return  "#"+str(self.id)+" - "+str(self.cliente) 

class PedidoArticulo(models.Model):
	pedido = models.ForeignKey(Pedido, related_name="PedidoArticulo_pedido", on_delete=models.PROTECT)
	articulo = models.ForeignKey(Articulo, related_name="PedidoArticulo_articulo", on_delete=models.PROTECT)
	cantidad = models.IntegerField(max_length=255)
	is_active = models.BooleanField(default=True)

