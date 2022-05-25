# from .models import Magnet
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from asgiref.sync import sync_to_async

path = os.getcwd()

# def magnet():
# 	file = open("main\\desloggs.log", "r")
# 	linelist = file.readlines()
# 	linelist = [ line[13 : -21] for line in linelist ]

# 	for link in linelist:
# 		try:
# 			obj = Magnet.objects.get(id = link[-2:], epub_link=link)
# 		except Magnet.DoesNotExist:
# 			obj = Magnet(id = link[-2:], epub_link=link)
# 		obj.save()



# def get_magnet():
# 	import re
# 	file = open("main\\desloggs.log", "r")
# 	linelist = file.readlines()
# 	linelist = [ line[:-21] for line in linelist ]
# 	from main.models import Magnet
# 	from main.models import Ebook
# 	links = []
	
# 	for item in linelist:
# 		item = item.split(" ")
# 		links.append(item[1])	

# 	ebooks = Ebook.objects.all()
# 	for a in links:
# 		try:
# 			last_digits = re.match('.*?([0-9]+)$', a).group(1)
# 			for x in ebooks:
# 				if x.id == int(last_digits):
# 				   x.epub = a	
# 		except:
# 			print(a)

# 	return ebooks
	
		


# def dame():
# 	import re
# 	file = open("main\\desloggs.log", "r")
# 	linelist = file.readlines()
# 	linelist = [ line[:-21] for line in linelist ]
# 	from main.models import Magnet
# 	from main.models import Ebook
# 	links = []
	
# 	for item in linelist:
# 		item = item.split(" ")
# 		links.append(item[1])	

# 	ebooks = Ebook.objects.all()
# 	ids = []
# 	form = [[],[]]
# 	ebooklist = []
# 	for a in links:
# 		try:
# 			last_digits = re.match('.*?([0-9]+)$', a).group(1)
# 			# form[0].append(int(last_digits))	
# 			# form[1].append(a)
# 			x = ebooks.get(id=int(last_digits))
# 			x.epub = a
# 			ebooklist.append(x)
			

# 			print(x)
# 		except:
# 			pass

# 	return ebooklist




def notify_client(pedido):
	print("requested_by y also_wants")
	print(pedido.requested_by, pedido.also_wants)
	client_mail = pedido.requested_by
	all_clients = []
	also_wants = pedido.also_wants
	if also_wants != None and " " in also_wants:
		also_wants = also_wants.split()
		all_clients += also_wants
		all_clients.append(client_mail)

	elif also_wants != None and " " in also_wants == False:
		all_clients.append(also_wants)
		all_clients.append(client_mail)


	from_mail = 'adoravant@gmail.com'
	to_mail = all_clients
	print("to_mail \n", to_mail)
	subject = f"Libronube | Pedido listo: {pedido.titulo}, {pedido.autor}"
	message = f"Estimado/a, \nSu pedido {pedido.titulo}, {pedido.autor}.\nPor favor certifique que el archivo que han subido corresponde al título solicitado.."
	#send_mail(subject, message, from_mail, to_mail, fail_silently=False)
	#html_message = render_to_string('base/donate.html')
	#plain_message = strip_tags(html_message)
	#send_mail(subject, plain_message, from_mail, to_mail, fail_silently=False, html_message=html_message)
	messages = [(subject, message, from_mail, [to]) for to in to_mail]
	send_mass_mail(messages)


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip
