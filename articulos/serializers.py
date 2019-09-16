from rest_framework import serializers
# models
from .models import Articulo, Marca

# serializers
class MarcaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Marca
		fields = ('id' ,'nombre')

class ArticuloSerializer(serializers.ModelSerializer):

	marca_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset = Marca.objects.all())
	marca = MarcaSerializer(read_only=True)

	class Meta:
		model = Articulo
		fields = ('id' ,'codigo', 'nombre', 'marca', 'marca_id')

		