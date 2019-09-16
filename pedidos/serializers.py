from rest_framework import serializers
# models
from .models import Pedido, Estado 
from  articulos.models import Articulo
from clientes.models import Cliente
# serializers
from articulos.serializers import ArticuloSerializer
from clientes.serializers import ClienteSerializer

class EstadoSerializer(serializers.ModelSerializer):

	class Meta:
		model = Estado
		fields = ('id' , 'nombre')

class PedidoSerializer(serializers.ModelSerializer):

	articulo_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset = Articulo.objects.all())
	articulo = ArticuloSerializer(read_only=True)

	cliente_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset = Cliente.objects.all())
	cliente = ClienteSerializer(read_only=True)

	estado_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset = Estado.objects.all())
	estado = EstadoSerializer(read_only=True)

	class Meta:
		model = Pedido
		fields = ('id' , 'cliente', 'cliente_id', 'articulo', 'articulo_id' , 'cantidad', 'estado', 'estado_id', 'is_active')