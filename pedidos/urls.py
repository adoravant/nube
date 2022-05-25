from django.urls import path, include, re_path
from django.contrib import admin
from . import views
from .views import delete_pedido, PedidoSearch, confirm_pedido, update_credit, add_favorite, misPedidosListView, abiertosListView, cerradosListView, pedidoListView, make_pedido, complete_pedido, add_me_pedido, update_vote_pedido


app_name = 'pedidos'  # here for namespacing of urls.


urlpatterns = [
path(r'pedidos-de-usuarios/', pedidoListView.as_view(), name="pedidos_list_view"),
path(r'pedidos/nuevo/', make_pedido, name="make_pedido"),
path(r'pedidos/complete/', complete_pedido, name="complete_pedido"),

path(r'pedidos/enviame/', add_me_pedido, name="add_me_pedido"),
path(r'pedidos/votar/', update_vote_pedido, name="update_vote_pedido"),
path(r'pedidos-completados-<str:order>/', cerradosListView.as_view(), name="cerrados_list_view"),
path(r'pedidos-abiertos-<str:order>/', abiertosListView.as_view(), name="abiertos_list_view"),
path(r'mis-pedidos-<str:order>/', misPedidosListView.as_view(), name="mis_pedidos_list_view"),
path(r'agregar-favoritos/', add_favorite, name="add_favorite"),
path(r'update-credit-<str:action>/', update_credit, name="update_credit"),
path(r'confirm-pedido/', confirm_pedido, name="confirm_pedido"),
path(r'pedidos/', PedidoSearch.as_view(), name="pedidos_search_view" ),
path(r'delete-<int:id_pedido>/', delete_pedido, name="delete_pedido" ),

]

