from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
# from main.models import Ebook, Genero, Tracker, ClientIp
from main.utils import get_client_ip
from accounts.models import Customer


@unauthenticated_user
def delayed_register(request):
	context = {}
	ip = get_client_ip(request)
	obj, create = ClientIp.objects.get_or_create(ip=ip)
	
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			#meto mano yo
			client_ip = ClientIp.objects.get(ip=ip)
			client_ip.paid = False
			client_ip.save()
			customer = Customer.objects.get(name=username)
			customer.ip = ip
			customer.daydownloads = client_ip.daydownloads
			customer.email = form.cleaned_data.get("email")
			customer.payment = client_ip.payment
			customer.save()
			messages.success(request, 'Nuevo usuario creado ' + username)
			login(request, user)	
			return redirect('accounts:login')
	
	context['form'] = form
	return render(request, 'accounts/register.html', context)


@unauthenticated_user
def registerPage(request):
	context = {}
	ip = get_client_ip(request)
	obj, create = ClientIp.objects.get_or_create(ip=ip)
	if obj.paid == True:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				#meto mano yo
				client_ip = ClientIp.objects.get(ip=ip)
				client_ip.paid = False
				client_ip.save()
				customer = Customer.objects.get(name=username)
				customer.ip = ip
				customer.daydownloads = client_ip.daydownloads
				customer.email = form.cleaned_data.get("email")
				customer.payment = client_ip.payment
				customer.save()
				messages.success(request, 'Nuevo usuario creado ' + username)
				login(request, user)	
				return redirect('accounts:login')
	else:
		return redirect("base:donate", args=9)		

	context['form'] = form
	return render(request, 'accounts/register.html', context)



@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('main:ebook_list')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {"generos": Genero.objects.values_list("name", flat=True).distinct()}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('accounts:login')

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {"seotags":Genero.objects.all(), "count" :Tracker.count ,"generos": Genero.objects.values_list("name", flat=True).distinct() ,'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending, "ebooks": Ebook.objects.all()[100:106]}
	return render(request, 'accounts/user.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {"count" :Tracker.count, 'form':form, "generos": Genero.objects.values_list("name", flat=True).distinct()}
	return render(request, 'accounts/account_settings.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {"count" :Tracker.count, 'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset, "count" :Tracker.count}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	print('ORDER:', order)
	if request.method == 'POST':

		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)




def dashBoard(request):
	orders = Order.objects.all().order_by('-status')[0:5]
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = Order.objects.all().count()
	delivered = Order.objects.filter(status='Delivered').count()
	pending = Order.objects.filter(status='Pending').count()



	context = {'customers':customers, 'orders':orders,
	'total_customers':total_customers,'total_orders':total_orders, 
	'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/dashboard.html', context)
	
