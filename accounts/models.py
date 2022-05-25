from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	ip = models.CharField(max_length=200, null=True)
	paid = models.BooleanField(default=False)
	payment = models.CharField(max_length=200, null=True)
	downloads = models.IntegerField(null=True, default=0)
	daydownloads = models.IntegerField(null=True, default=5)
	lastdownload = models.DateTimeField(null=True, blank=True)
	pedidos = models.IntegerField(default=0, null=True, blank=True)
	pidio = models.TextField(max_length=50, null=True, blank=False)
	add_me_pedido = models.TextField(max_length=200, null=True, blank=False)
	pedidos_liked = models.TextField(max_length=50, null=True, blank=False)
	viewed = models.TextField(max_length=50, null=True, blank=False)
	liked =  models.TextField(max_length=50, null=True, blank=False)
	downloaded = models.TextField(max_length=50, null=True, blank=False)
	#current_pedidos_completed = models.IntegerField(null=True, default=0)
	#last_pedidos_completed = models.IntegerField(null=True, default=0)

	def list_and_len(self, campo=None):
		items = campo.split(" ")
		return items, len(items)

	def update_client(self, pidio=None, email=None, liked=None, viewed=None, add_me_pedido=None, pedidos=None, downloads=None, downloaded=None, lastdownload=None, pedidos_liked=None):   
		if email != None:
			self.email = email
		if liked != None:
			if self.liked == None:
				self.liked = liked
			elif liked not in self.liked:
				self.liked += f" {liked}"
		if viewed != None:
			if self.viewed == None:
				self.viewed = viewed
			elif viewed not in self.viewed:
				self.viewed += f" {viewed}"

		if add_me_pedido != None:
			if self.add_me_pedido == None:
				self.add_me_pedido = add_me_pedido
			elif add_me_pedido not in self.add_me_pedido:
				self.add_me_pedido += f" {add_me_pedido}"
				

		if pedidos_liked != None:
			if self.pedidos_liked == None:
				self.pedidos_liked = pedidos_liked
			elif pedidos_liked not in self.pedidos_liked:
				self.pedidos_liked += f" {pedidos_liked}"                       

		if downloaded != None:
			if self.downloaded == None:
				self.downloaded = downloaded
			elif downloaded not in self.downloaded:
				self.downloaded += f" {downloaded}"         

		
		if pidio != None:
			if self.pidio == None:
				self.pidio = pidio
			else:
				self.pidio += f" {pidio}"        


		if pedidos != None:
			self.pedidos += 1


		if downloads != None:
			self.downloads += 1

		if lastdownload != None:
			self.lastdownload = datetime.now()

		self.save()     





	def __str__(self):
		return self.name








class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.product.name



	
