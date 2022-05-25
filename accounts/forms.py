from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _
from .models import *

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = ["name", "phone", "email", "profile_pic"]
		exclude = ['user']

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
        	super().__init__(*args, **kwargs)
        	self.fields['username'].widget.attrs.update({'placeholder':_('Usuario')})
        	self.fields['email'].widget.attrs.update({'placeholder':_('Correo')})
        	self.fields['password1'].widget.attrs.update({'placeholder':_('Contraseña')})        
        	self.fields['password2'].widget.attrs.update({'placeholder':_('Confirma contraseña')})
