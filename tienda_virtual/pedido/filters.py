from django_filters import rest_framework as filters
from .models import Pedido

class filtrarPedido(filters.FilterSet):

    class Meta:
        model = Pedido
        fields = ('id', 'estado', 'estado_pago', 'modo_pago')