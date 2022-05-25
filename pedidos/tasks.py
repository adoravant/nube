from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail, send_mass_mail
from celery import shared_task
from .models import Pedido

@shared_task
def sleepy():
    lista = ["adoravant@gmail.com", "libronube.com@gmail.com"]
    for a in range(10):
         send_mail("enviado desde task", "bien papewen", "adoravant@gmail.com", lista, fail_silently=False)


@shared_task
def notify_client(id_pedido):
	pedido = Pedido.objects.get(id=id_pedido)
	from_mail = 'libronube.com@gmail.com'
	to_mail = get_recipients(pedido)
	subject = f"Libronube | Pedido listo: {pedido.titulo}, {pedido.autor}"
	message = f"Estimado/a, \nSu pedido {pedido.titulo}, {pedido.autor} está listo!.\nPor favor corrobore que el archivo que han subido corresponde al título solicitado..\nlibronube.com/pedidos-completados-recientes"
	messages = [(subject, message, from_mail, [to]) for to in to_mail]
	send_mass_mail(messages, fail_silently=False)



def get_recipients(pedido):
	also_wants = pedido.also_wants
	all_clients = [pedido.requested_by]
	print("also_wants", also_wants)
	if also_wants != None:
		if " " in also_wants:
			also_wants = also_wants.split()
			all_clients = all_clients + also_wants
			print("also_wants with spaces")
		else:
			print("also_wants no spaces")
			all_clients.append(also_wants)
			
	return all_clients			 




