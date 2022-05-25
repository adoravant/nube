from django.db import models
from django.utils.timezone import now
from unidecode import unidecode
from main.models import *
from accounts.models import Customer
# Create your models here.

class Pedido(models.Model):
	titulo = models.CharField(max_length=200, blank=True, null=True)
	autor = models.CharField(max_length=200, blank=True, null=True)
	completed_by = models.CharField(max_length=200, blank=True, null=True, default="me")
	requested_by = models.EmailField(max_length=200, blank=True, null=True, default="me")
	pdf = models.FileField(blank=True, null=True, max_length=100, upload_to="pedidos/pdfs/")
	ip = models.CharField(max_length=200, blank=True, null=True, default="me")
	votos = models.IntegerField(default=0, blank=True, null=True)
	completed = models.BooleanField(default=False)
	checked = models.BooleanField(default=False)
	sent = models.BooleanField(default=False)
	also_wants = models.TextField(max_length=5000, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified = models.DateTimeField(auto_now=True, null=True, blank=True)
	unidecode_titulo = models.CharField(max_length=200, blank=True, null=True)
	unidecode_autor =  models.CharField(max_length=200, blank=True, null=True)
	# client_ip = models.ForeignKey(ClientIp, null=True, blank=True, on_delete=models.SET_NULL)
	#+customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)	
	# epub = models.ForeignKey(Epub, null=True, blank=True, on_delete=models.SET_NULL)
	#book = models.ForeignKey(Ebook, null=True, blank=True, on_delete=models.SET_NULL)	


	#def save(self, *args, **kwargs):
		#if not self.id:
			#self.created = now()
			#self.unidecode_titulo = unidecode(self.titulo)
			#self.unidecode_autor = unidecode(self.autor)
		#self.modified = now() 
		#super(Pedido, self).save(*args, **kwargs)    



	def __str__(self):
		if self.titulo != None:
			return self.titulo
		else:
			return str(self.id)		
	

	def get_also_wants(self):
		try:
			also_wants_list = self.also_wants.split(" ")		
			return also_wants_list
		except:
			pass

	def add_also_wants(self, email):
		if self.also_wants == None:
			self.also_wants = email
		else:
			self.also_wants += f" {email}"
		self.save()


			
