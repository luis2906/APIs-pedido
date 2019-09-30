# App
from ujueta.structure_response import Structure

# django
from django.db import IntegrityError,transaction
from django.db.models import Q
# rest_framework
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
# json
import json


# models
from helpers.bulk_create_manage import BulkCreateManager
from .models import Pedido, Estado,PedidoArticulo
# serializers
from .serializers import PedidoSerializer, EstadoSerializer, PedidoArticuloSerializer

# Create your views here.
class PedidoViewSet(viewsets.ModelViewSet):

	model = Pedido
	queryset = model.objects.all()
	serializer_class = PedidoSerializer
	parser_classes=(FormParser, MultiPartParser)
	nombre_modulo = 'Pedido.PedidoViewSet'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Structure.success_200('', serializer.data)	

		except Exception as e:			
			return Structure.error_400('No se encontraron registros')

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(PedidoViewSet, self).get_queryset()
			page = self.request.query_params.get('page', None)
			filter_data = self.request.query_params.get('filter_data', None)
            # --------------------------------------------------------------
			cliente_id = self.request.query_params.get('cliente_id',None)
			is_active = self.request.query_params.get('is_active',True)
			
			qset=(~Q(id=0))
			
			if (filter_data or cliente_id or is_active):
				if filter_data:
					qset = qset & (Q(name__icontains = filter_data) )
				if cliente_id:
					qset = qset & (Q(cliente__id = cliente_id) )

				if is_active:
					qset = qset & (Q(is_active = is_active) )
				
				queryset = self.model.objects.filter(qset)

			if page:						
				pagination = self.paginate_queryset(queryset)			
				if pagination is not None:
					serializer = self.get_serializer(pagination, many=True)
					return self.get_paginated_response(serializer.data)
				
			serializer = self.get_serializer(queryset,many=True)
			return Structure.success_200('', serializer.data)

		except Exception as e:
			print(e)
			return Structure.error_500()

	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			try:

				json_data = json.loads(request.body)
				serializer = self.serializer_class(data=json_data,context={'request': request})
				if serializer.is_valid():
					serializer.save(cliente_id = json_data["cliente_id"],
									estado_id = json_data["estado_id"]
									)
				
					bulk_mgr = BulkCreateManager(chunk_size=1)
					for row in json_data["articulos"]:
						bulk_mgr.add(PedidoArticulo(pedido_id=serializer.data['id'], articulo_id=row['id'], cantidad=row['cantidad'] ))
					bulk_mgr.done()

					return Structure.success_201('El pedido #{} ha sido registrado exitosamente.'.format(serializer.data["id"]), serializer.data)
				else:
					print(serializer.errors)
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
					serializer.save(articulo_id = json_data['articulo_id'], 
									cliente_id = json_data['cliente_id'],
									estado_id = json_data['estado_id']
									)			
					return Structure.success_201('El pedido ha sido actualizado exitosamente.', serializer.data)
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
				return Structure.success_204('El pedido ha sido eliminado exitosamente.', serializer.data)
			except Exception as e:
				return Structure.error_500()

	@action(methods=['PUT'], detail=False, url_path='delete', url_name='delete.pedido')	
	def delete(self,request,*args,**kwargs):
		
		if request.method == 'PUT':
			json_data = json.loads(request.body)			
			try:
				index = json_data["index"]
				pedido = Pedido.objects.filter(pk__in=index).update(is_active=False)		
				return Structure.success_201('Los pedidos han sido eliminado exitosamente.', '')

			except Exception as e:
				return Structure.error_500()

class EstadoViewSet(viewsets.ModelViewSet):

	model = Estado
	queryset = model.objects.all()
	serializer_class = EstadoSerializer
	parser_classes=(FormParser, MultiPartParser)
	nombre_modulo = 'Estado.EstadoViewSet'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Structure.success_200('', serializer.data)	

		except Exception as e:			
			return Structure.error_400('No se encontraron registros')

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(EstadoViewSet, self).get_queryset()
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


class PedidoArticuloViewSet(viewsets.ModelViewSet):

	model = PedidoArticulo
	queryset = model.objects.all()
	serializer_class = PedidoArticuloSerializer
	parser_classes=(FormParser, MultiPartParser)
	nombre_modulo = 'PedidoArticulo.PedidoArticuloViewSet'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Structure.success_200('', serializer.data)	

		except Exception as e:			
			return Structure.error_400('No se encontraron registros')

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(PedidoArticuloViewSet, self).get_queryset()
			page = self.request.query_params.get('page', None)
			filter_data = self.request.query_params.get('filter_data', None)
            # --------------------------------------------------------------
			pedido_id = self.request.query_params.get('pedido_id',None)
			articulo_id = self.request.query_params.get('articulo_id',True)
			
			qset=(~Q(id=0))
			
			if (filter_data or pedido_id or articulo_id):
				if filter_data:
					qset = qset & (Q(name__icontains = filter_data) )
				if pedido_id:
					qset = qset & (Q(pedido__id = pedido_id) )

				if articulo_id:
					qset = qset & (Q(articulo__id = articulo_id) )
				
				queryset = self.model.objects.filter(qset)

			if page:						
				pagination = self.paginate_queryset(queryset)			
				if pagination is not None:
					serializer = self.get_serializer(pagination, many=True)
					return self.get_paginated_response(serializer.data)
				
			serializer = self.get_serializer(queryset,many=True)
			return Structure.success_200('', serializer.data)

		except Exception as e:
			print(e)
			return Structure.error_500()

	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			try:

				json_data = json.loads(request.body)
				serializer = self.serializer_class(data=json_data,context={'request': request})
				if serializer.is_valid():
					serializer.save(pedido_id = json_data["pedido_id"], 
									articulo_id = json_data["articulo_id"]
									)
					return Structure.success_201('El articulo ha sido registrado exitosamente.', serializer.data)
				else:
					print(serializer.errors)
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
					serializer.save(pedido_id = json_data["pedido_id"], 
									articulo_id = json_data["articulo_id"]
									)			
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

