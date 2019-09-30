from django.contrib import admin

# Register your models here.
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'apellido')


admin.site.register(Cliente, ClienteAdmin)