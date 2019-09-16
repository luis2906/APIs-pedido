from django.db import models

# Create your models here.
class Cliente(models.Model):

	numero_identificacion = models.BigIntegerField(unique=True)
	nombre = models.CharField(max_length=255)
	apellido = models.CharField(max_length=255)
	
	def __str__(self):
		return self.nombre 