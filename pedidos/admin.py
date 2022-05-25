from django.contrib import admin
from .models import Pedido
# Register your models here.



class PedidoAdmin(admin.ModelAdmin):
	pass

admin.site.register(Pedido, PedidoAdmin)
# admin.site.register(Autor, AutorAdmin)


