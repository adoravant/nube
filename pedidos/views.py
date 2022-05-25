from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from .models import Pedido
from main.models import *
from .forms import PedidoUploadForm
from django.db.models import Max
from random import randint
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import json
from main.utils import notify_client
from .tasks import notify_client
from django.db.models import Q
from unidecode import unidecode


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip




# def get_to_know_you(request):
# 	if request.user.is_authenticated:
# 		download_info = True
# 		return download_info
# 	ip = get_client_ip(request)
# 	obj, created = ClientIp.objects.get_or_create(ip=ip)

# 	if created:
# 		download_info = True  
# 	else:
# 		if obj.downloads >= 2:
# 			if not obj.lastdownload or (timezone.now() - obj.lastdownload).days >= 7:
# 				download_info = True  
# 			else:
# 				passed = timezone.now() - obj.lastdownload
# 				int_next_download = (timedelta(days=7) - passed).days
# 				if int_next_download == 0:
# 					next_download = timedelta(days=7) - passed
# 					hours, remainder = divmod(next_download.total_seconds(), 3600)
# 					minutes, seconds = divmod(remainder, 60)  
# 					download_info = f"{hours}:{minutes}".replace(".0", "")
# 				else:
# 					download_info =  (timedelta(days=7) - passed).days
# 		else:
# 			download_info = True

# 	return download_info











def delete_pedido(request, id_pedido):
	pedido = Pedido.objects.get(id=id_pedido).delete()
	previous_url = request.META.get('HTTP_REFERER')
	return redirect(previous_url)




def make_pedido(request):
	if request.method == "POST":
		form = PedidoUploadForm(request.POST)
		if form.is_valid():
			form.save()
			ip = request.POST.get('ip')
			pedido = Pedido.objects.filter(titulo=form.cleaned_data['titulo']).last()
			if request.user.is_authenticated == False:
				#RETURN REDIRECT
				pass
			else:
				#pendiente update_customer
				pedido.customer = request.user.customer
			pedido.save()	
			messages.info(request, f"Pedido '{form.cleaned_data['titulo']}' creado")
			return redirect('pedidos:abiertos_list_view', request.session.get("order"))

		else:
			messages.error(request, f"email '{form.data['requested_by']}' no es un email valido")
	else:
		form = PedidoUploadForm()
	return redirect('pedidos:abiertos_list_view', request.session.get("order"))


def add_favorite(request):
	ebook_id = request.session.get("last_viewed_book")
	ebook = Ebook.objects.get(id=ebook_id)
	ip = get_client_ip(request)
	
	
	# obj, created = ClientIp.objects.get_or_create(ip=ip)
	# obj.update_client(liked=str(ebook_id))
	previous_url = request.META.get('HTTP_REFERER')
	return redirect(previous_url)




def complete_pedido(request):
	if request.method == "POST":
		file = request.FILES['docfile']
		id_pedido = request.POST.get('id')
		completed_by = request.POST.get('completed_by')
		fs = FileSystemStorage()
		
		if file.name.endswith(".pdf") or file.name.endswith(".epub") or file.name.endswith(".mobi"):
			file = fs.save(f"pedidos/files/{file.name}", file)
			url = fs.url(file)
			pedido = Pedido.objects.get(id=id_pedido)
			pedido.completed_by = completed_by
			pedido.completed = True
			pedido.pdf = file
			pedido.save()
			notify_client.delay(id_pedido)
			messages.info(request, f"Pedido '{pedido.titulo}' completado")
			#enviar mail a al que pidio y a los que se agregaron al pedido
			return redirect('pedidos:abiertos_list_view', request.session.get("order"))	
		else:
			#message error	    	
			return redirect("pedidos:abiertos_list_view")		



class pedidoListView(ListView):
	paginate_by = 100
	model = Pedido
	queryset = Pedido.objects.all().order_by("-votos")
	context_object_name = "pedidos"
	template_name = "pedidos/pedido_list.html"	

	def get_context_data(self, **kwargs):
		context = super(pedidoListView, self).get_context_data(**kwargs)     
		context['generos'] = Genero.objects.values_list("name", flat=True).distinct(
		).order_by("name")
		context['seotags'] = Genero.objects.all()
		context['client_ip'] = get_client_ip(self.request)
		# obj, created = ClientIp.objects.get_or_create(ip=context['client_ip'])
		# context['ip_object'] = obj
		# context['top_vote'] = Pedido.objects.all().order_by('-votos')[0].votos + randint(99,150)
		try:
			tab = self.request.session.get('tab')
			print("trytab", tab)
		except:
			tab = None
		current_url = self.request.path
		print("current_url", current_url)
		context['tab'] = tab
		return context





def add_me_pedido(request):
	if request.method == "POST":
		id_pedido = request.POST.get('id')
		print(id_pedido)
		email = request.POST.get('also_wants')
		ip = request.POST.get('ip')
		#sumarle el also_wants al pedido.
		pedido = Pedido.objects.get(id=id_pedido)
		pedido.add_also_wants(email)
		#sumarle el add_me_pedido al IP
		# obj, created = ClientIp.objects.get_or_create(ip=ip)
		# obj.update_client(add_me_pedido=id_pedido, email=email)
		messages.success(request, f"Recibirás '{pedido.titulo}' en tu correo.")
		
		return redirect("pedidos:abiertos_list_view", request.session.get("order"))
		
	else:	    	
		return redirect("pedidos:abiertos_list_view")




def update_vote_pedido(request):
	data = json.loads(request.body)
	pedido_id = data ['productId']
	action = data['action']
	pedido = Pedido.objects.get(id=pedido_id)
	ip = get_client_ip(request)
	# obj, created = ClientIp.objects.get_or_create(ip=ip)
	# obj.update_client(pedidos_liked=pedido_id)
	# if action == 'add':
	# 	pedido.votos = (pedido.votos + 1)
	# if action == 'remove':
	# 	pedido.votos = (pedido.votos - 1)
	pedido.save()		
	if request.session.get('tab') == "abiertos":
		return redirect("pedidos:abiertos_list_view")
	else:
		return redirect("pedidos:cerrados_list_view")
	





class cerradosListView(ListView):
	paginate_by = 50
	model = Pedido
	queryset = Pedido.objects.filter(completed=True).order_by("-votos")
	context_object_name = "pedidos"
	template_name = "pedidos/pedido_list.html"	

	def get_context_data(self, **kwargs):
		context = super(cerradosListView, self).get_context_data(**kwargs)     
		context['generos'] = Genero.objects.values_list("name", flat=True).distinct(
		).order_by("name")
		context['seotags'] = Genero.objects.all()
		context['client_ip'] = get_client_ip(self.request)
		# obj, created = ClientIp.objects.get_or_create(ip=context['client_ip'])
		# context['ip_object'] = obj
		# context['top_vote'] = Pedido.objects.all().order_by('-votos')[0].votos + randint(99,150)
		self.request.session['tab'] = "cerrados"
		context['tab'] = "cerrados"
		context['order'] = self.request.session.get('order')
		# obj, created = ClientIp.objects.get_or_create(ip=context['client_ip'])
		# if obj.email != None:
		# 	context['email'] = obj.email	
		# else:
		# 	context['email'] = "vacio"
		return context



	
	def get_queryset(self, *args, **kwargs):
		queryset = super().get_queryset()
		order = self.kwargs['order']
		if order == "likes":
			queryset = Pedido.objects.filter(completed=True).order_by("-votos")

		elif order == "recientes":
			queryset = Pedido.objects.filter(completed=True).order_by("-modified")

		
		elif order == "titulo":
			print("entre orden titulo")
			queryset = Pedido.objects.filter(completed=True).order_by("titulo")
		
		elif order == "autor":
			queryset = Pedido.objects.filter(completed=True).order_by("autor")

		self.request.session['order'] = order
		print("order", order)
		return queryset	
		









class abiertosListView(ListView):
	paginate_by = 50
	model = Pedido
	queryset = Pedido.objects.filter(completed=False).order_by("-votos")
	context_object_name = "pedidos"
	template_name = "pedidos/pedido_list.html"	

	def get_context_data(self, **kwargs):
		context = super(abiertosListView, self).get_context_data(**kwargs)     
		context['generos'] = Genero.objects.values_list("name", flat=True).distinct(
		).order_by("name")
		context['seotags'] = Genero.objects.all()
		context['client_ip'] = get_client_ip(self.request)
		# obj, created = ClientIp.objects.get_or_create(ip=context['client_ip'])
		# context['ip_object'] = obj
		# context['top_vote'] = Pedido.objects.all().order_by('-votos')[0].votos + randint(21,41)
		self.request.session['tab'] = "abiertos"
		current_url = self.request.path
		context['tab'] = "abiertos"
		# obj, created = ClientIp.objects.get_or_create(ip=context['client_ip'])
		try:
			context['order'] = self.request.session.get('order')
		except:
			context['order'] = "recientes"
		# if obj.email != None:
		# 	context['email'] = obj.email	
		# else:
		# 	context['email'] = "vacio"
		return context



	def get_queryset(self, *args, **kwargs):
		queryset = super().get_queryset()
		order = self.kwargs['order']
		if order == "likes":
			queryset = Pedido.objects.filter(completed=False).order_by("-votos")

		elif order == "recientes":
			queryset = Pedido.objects.filter(completed=False).order_by("-created")

		
		elif order == "titulo":
			print("entre orden titulo")
			queryset = Pedido.objects.filter(completed=False).order_by("titulo")
		
		elif order == "autor":
			queryset = Pedido.objects.filter(completed=False).order_by("autor")

		self.request.session['order'] = order
		print("order", order)
		return queryset






class misPedidosListView(ListView):
	paginate_by = 50
	model = Pedido
	queryset = Pedido.objects.filter(completed=True).order_by("-votos")
	context_object_name = "pedidos"
	template_name = "pedidos/pedido_list.html"	

	def get_context_data(self, **kwargs):
		context = super(misPedidosListView, self).get_context_data(**kwargs)     
		context['generos'] = Genero.objects.values_list("name", flat=True).distinct(
		).order_by("name")
		context['seotags'] = Genero.objects.all()
		context['client_ip'] = get_client_ip(self.request)
		# obj, created = ClientIp.objects.get_or_create(ip=context['client_ip'])
		# context['ip_object'] = obj
		# context['top_vote'] = Pedido.objects.all().order_by('-votos')[0].votos + randint(99,150)
		self.request.session['tab'] = "mis pedidos"
		context['tab'] = "mis pedidos"
		context['order'] = self.request.session.get('order')
		# obj, created = ClientIp.objects.get_or_create(ip=context['client_ip'])
		# if obj.email != None:
		# 	context['email'] = obj.email	
		# else:
		# 	context['email'] = "vacio"
		return context



	
	def get_queryset(self, *args, **kwargs):
		queryset = super().get_queryset()
		order = self.kwargs['order']
		ip = get_client_ip(self.request)
		print("ip", ip)
		if order == "likes":
			queryset = Pedido.objects.filter(ip=ip).order_by("-votos")

		elif order == "recientes":
			queryset = Pedido.objects.filter(ip=ip).order_by("-created")
                        #hay que mejorar trayendo lo mismo que use en users.html
		
		elif order == "titulo":
			print("entre orden titulo")
			queryset = Pedido.objects.filter(ip=ip).order_by("titulo")
		
		elif order == "autor":
			queryset = Pedido.objects.filter(ip=ip).order_by("autor")

		self.request.session['order'] = order
		print("order", order)
		return queryset	



def update_credit(request, action):
	obj, created = ClientIp.objects.get_or_create(ip=get_client_ip(request))
	obj.update_client(credits=action)
	previous_url = request.META.get('HTTP_REFERER')
	return redirect(previous_url)


def confirm_pedido(request):
	id_pedido = request.POST.get('id')
	confirm = request.POST.get('confirm')
	pedido = Pedido.objects.get(id=id_pedido)
	obj, created = ClientIp.objects.get_or_create(ip=pedido.completed_by)
	if confirm == "ES CORRECTO":
		pedido.checked = True
		obj.update_client(credits="add")
		#send mail pedido.requested_by confirmando el pedido	
	
	else:
		pedido.completed = False
		pedido.pdf = ""
		obj.update_client(credits="remove")
		print("EL FUCKING ARCHIVO ES INCORRECTO")
	
	pedido.save()	


	
	
	
	
	
	previous_url = request.META.get('HTTP_REFERER')
	return redirect(previous_url)




class PedidoSearch(ListView):
	template_name = "pedidos/pedido_list.html"
	queryset =  Pedido.objects.first()       
	
	def get_context_data(self, **kwargs):
		context = super(PedidoSearch, self).get_context_data(**kwargs)
		query1 = self.request.GET.get('q')          
		query1 = unidecode(query1)
		context['generos'] = Genero.objects.values_list("name", flat=True).distinct()
		context['seotags'] = Genero.objects.all()
		criterio1 = Q(titulo__iregex=r"\b{0}\b".format(query1))
		criterio2 = Q(autor__iregex=r"\b{0}\b".format(query1))
		# context['titulo'] = Epub.objects.filter(reduce(operator.and_, (Q(unidecode_titulo__iregex=r"\b{0}\b".format(x)) for x in querie)))[:19]
		context['pedidos'] = Pedido.objects.filter(criterio1 | criterio2)[:19]
		context['pedidos_search_view'] = True
		context['order'] = self.request.session.get("order")
		context['query1'] = query1
		print(not context['pedidos'])
		return context
