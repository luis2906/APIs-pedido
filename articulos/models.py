from django.db import models

# Create your models here.
class BaseModel(models.Model):
	nombre = models.CharField(unique=True, max_length=255)
	class Meta:
		abstract = True

	def __str__(self):
		return self.nombre

class Marca(BaseModel):

	pass
	
	def __str__(self):
		return self.nombre 

class Articulo(BaseModel):

	codigo = models.CharField(unique=True, max_length=255)
	marca = models.ForeignKey(Marca, related_name="Articulo_marca", on_delete=models.PROTECT)
	
	def __str__(self):
		return self.nombre 