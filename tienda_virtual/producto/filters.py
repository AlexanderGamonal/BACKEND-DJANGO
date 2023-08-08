from django_filters import rest_framework as filters
from .models import Producto

class ProductosFilter(filters.FilterSet):

    p_clave = filters.CharFilter(field_name="nombre", lookup_expr="icontains")
    min_price = filters.NumberFilter(field_name="precio" or 0, lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="precio" or 1000000, lookup_expr="lte")

    class Meta:
        model = Producto
        fields = ('p_clave', 'categoria', 'marca', 'min_price', 'max_price')