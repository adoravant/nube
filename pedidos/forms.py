from django.forms import ModelForm
from django import forms
from pedidos.models import Pedido



class PedidoUploadForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ("titulo", "autor", "requested_by", "ip", "votos",)



class PedidoAddMeForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ("also_wants",)


class PedidoCompleteForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ("pdf",)