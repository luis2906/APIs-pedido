# App
from ujueta.structure_response import Structure

# django
from django.db import IntegrityError,transaction
from django.db.models import Q
# rest_framework
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
# json
import json


# models
from .models import Cliente
# serializers
from .serializers import ClienteSerializer

# Create your views here.
class ClienteViewSet(viewsets.ModelViewSet):

	model = Cliente
	queryset = model.objects.all()
	serializer_class = ClienteSerializer
	parser_classes=(FormParser, MultiPartParser)
	nombre_modulo = 'Cliente.ClienteViewSet'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Structure.success_200('', serializer.data)	

		except Exception as e:			
			return Structure.error_400('No se encontraron registros')

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(ClienteViewSet, self).get_queryset()
			page = self.request.query_params.get('page', None)
			filter_data = self.request.query_params.get('filter_data', None)
            # --------------------------------------------------------------
			nombre = self.request.query_params.get('nombre',None)
			apellido = self.request.query_params.get('apellido',None)
			
			qset=(~Q(id=0))
			
			if (filter_data or nombre or apellido):
				if filter_data:
					qset = qset & (Q(nombre__icontains = filter_data) )
				if nombre:
					qset = qset & (Q(nombre = nombre) )
				if apellido:
					qset = qset & (Q(apellido = apellido) )
				
				queryset = self.model.objects.filter(qset)

			if page:						
				pagination = self.paginate_queryset(queryset)			
				if pagination is not None:
					serializer = self.get_serializer(pagination, many=True)
					return self.get_paginated_response(serializer.data)
				
			serializer = self.get_serializer(queryset,many=True)
			return Structure.success_200('', serializer.data)

		except Exception as e:
			return Structure.error_500()

	
	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			try:

				json_data = json.loads(request.body)
				serializer = self.serializer_class(data=json_data,context={'request': request})
				if serializer.is_valid():
					serializer.save()
					return Structure.success_201('El cliente ha sido registrado exitosamente.', serializer.data)
				else:
					return Structure.fail('', serializer.errors)
			
			except Exception as e:
				print(e)
				return Structure.error_500()

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':			
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				json_data = json.loads(request.body)
				serializer = self.serializer_class(instance, data=json_data, context={'request': request}, partial=partial)
				
				if serializer.is_valid():
					serializer.save()
					return Structure.success_201('El cliente ha sido actualizado exitosamente.', serializer.data)
				else:

					return Structure.fail('', serializer.errors)

			except Exception as e:
				return Structure.error_500()
