from django.contrib import admin

# Register your models here.
from .models import Articulo, Marca

class ArticuloAdmin(admin.ModelAdmin):
	list_display = ('nombre', )

class MarcaAdmin(admin.ModelAdmin):
	list_display = ('nombre', )


admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Marca, MarcaAdmin)
