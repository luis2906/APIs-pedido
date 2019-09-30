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
from .models import Articulo, Marca
# serializers
from .serializers import ArticuloSerializer, MarcaSerializer

# Create your views here.
class MarcaViewSet(viewsets.ModelViewSet):

	model = Marca
	queryset = model.objects.all()
	serializer_class = MarcaSerializer
	parser_classes=(FormParser, MultiPartParser)
	nombre_modulo = 'Marca.MarcaViewSet'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Structure.success_200('', serializer.data)	

		except Exception as e:			
			return Structure.error_400('No se encontraron registros')

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(MarcaViewSet, self).get_queryset()
			page = self.request.query_params.get('page', None)
			filter_data = self.request.query_params.get('filter_data', None)
            # --------------------------------------------------------------
			name = self.request.query_params.get('name',None)
			
			qset=(~Q(id=0))
			
			if (filter_data or name):
				if filter_data:
					qset = qset & (Q(name__icontains = filter_data) )
				if name:
					qset = qset & (Q(name = name) )
				
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


class ArticuloViewSet(viewsets.ModelViewSet):

	model = Articulo
	queryset = model.objects.all()
	serializer_class = ArticuloSerializer
	parser_classes=(FormParser, MultiPartParser)
	nombre_modulo = 'Articulo.ArticuloViewSet'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Structure.success_200('', serializer.data)	

		except Exception as e:			
			return Structure.error_400('No se encontraron registros')

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(ArticuloViewSet, self).get_queryset()
			page = self.request.query_params.get('page', None)
			filter_data = self.request.query_params.get('filter_data', None)
            # --------------------------------------------------------------
			name = self.request.query_params.get('name',None)
			
			qset=(~Q(id=0))
			
			if (filter_data or name):
				if filter_data:
					qset = qset & (Q(name__icontains = filter_data) )
				if name:
					qset = qset & (Q(name = name) )
				
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
				# Validate 
				serializer = self.serializer_class(data=request.data,context={'request': request})
				if serializer.is_valid():
					serializer.save(marca_id = request.data['marca_id'])
					return Structure.success_201('El articulo ha sido registrado exitosamente.', serializer.data)
				else:
					return Structure.fail('', serializer.errors)
			
			except Exception as e:
				return Structure.error_500()

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':			
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				serializer = self.serializer_class(instance, data=request.data, context={'request': request}, partial=partial)
				
				if serializer.is_valid():
					serializer.save(empresa_id=request.data['empresa_id'])				
					return Structure.success_201('El articulo ha sido actualizado exitosamente.', serializer.data)
				else:

					return Structure.fail('', serializer.errors)

			except Exception as e:
				return Structure.error_500()
							
	def destroy(self,request,*args,**kwargs):
		if request.method == 'DELETE':			
			try:
				instance = self.get_object()
				self.perform_destroy(instance)
				serializer = self.get_serializer(instance)
				return Structure.success_204('El articulo ha sido eliminado exitosamente.', serializer.data)
			except Exception as e:
				return Structure.error_500()