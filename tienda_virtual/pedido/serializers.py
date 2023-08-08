from rest_framework import serializers
from .models import Pedido, ArticuloPedido


class ArticuloPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloPedido
        fields = "__all__"


class PedidoSerializer(serializers.ModelSerializer):

    articulosPedidos = serializers.SerializerMethodField(method_name='get_articulos_pedidos', read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

    def get_articulos_pedidos(self, obj):
        articulos_pedidos = obj.articulospedidos.all()
        serializer = ArticuloPedidoSerializer(articulos_pedidos, many=True)
        return serializer.data
