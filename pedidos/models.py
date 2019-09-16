from django.db import models

from articulos.models import Articulo
from clientes.models import Cliente
# Create your models here.

class Estado(models.Model):
	nombre = models.CharField(unique=True, max_length=255)

	def __str__(self):
		return self.nombre 
	
class Pedido(models.Model):

	articulo = models.ForeignKey(Articulo, related_name="Pedido_articulo", on_delete=models.PROTECT)
	cliente = models.ForeignKey(Cliente, related_name="Pedido_cliente", on_delete=models.PROTECT)
	cantidad = models.IntegerField(max_length=255)
	estado = models.ForeignKey(Estado, related_name="Pedido_estado", on_delete=models.PROTECT)
	is_active = models.BooleanField(default=True)
