from rest_framework import serializers
# models
from .models import Cliente

# serializers
class ClienteSerializer(serializers.ModelSerializer):

	class Meta:
		model = Cliente
		fields = ('id' , 'numero_identificacion', 'nombre' ,'apellido')