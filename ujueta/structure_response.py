# rest_framework
from rest_framework.response import Response
from rest_framework import status

class Structure:
	"""docstring for Estructura"""
	@staticmethod
	def success_200(message, data):
		return Response({'status':'success', 'message':message, 'data':data}, status=status.HTTP_200_OK)

	@staticmethod
	def success_201(message, data):
		return Response({'status':'success', 'message':message, 'data':data}, status=status.HTTP_201_CREATED)

	@staticmethod
	def success_204(message, data):
		return Response({'status':'success', 'message':message, 'data':data}, status=status.HTTP_204_NO_CONTENT)

	@staticmethod
	def error_400(message):
		return Response({'status':'error', 'message':message, 'data':None}, status=status.HTTP_400_BAD_REQUEST)

	@staticmethod
	def fail(message, data=None):
		return Response({'status':'fail', 'message':message, 'error':data}, status=status.HTTP_400_BAD_REQUEST)

	@staticmethod
	def error_500(e=None):
		return Response({'status':'error', 
				'message':'Se presentaron errores de comunicacion con el servidor, consulte con el administrador del sistema.',
				'data':None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)	