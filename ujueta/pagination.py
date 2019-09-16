from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import status

class CustomPagination(pagination.PageNumberPagination):

	page_size_query_param = 'page_size'
	
	def get_paginated_response(self, data):
		
		paginacion = {	
			'total': self.page.paginator.count,		
			'per_page': self.page.paginator.per_page,
			'current_page': self.page.number,
			'total_pages': self.page.paginator.num_pages,
			'next': self.get_next_link(),
			'previous': self.get_previous_link(),			
			'status':'success',
			'data': data
		}

		return Response(paginacion, status=status.HTTP_200_OK)
