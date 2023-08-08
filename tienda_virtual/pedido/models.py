from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from producto.models import Producto

# Create your models here.

class EstadoPedido(models.TextChoices):
    ENPROCESO = 'En Proceso'
    ENVIADO = 'Enviado'
    ENTREGADO = 'Entregado'

class EstadoPago(models.TextChoices):
    PAGADO = 'PAGADO'
    SINPAGAR ='SIN PAGAR'

class ModoPago(models.TextChoices):
    COD = 'COD'
    TARJETA = 'TARJETA'


class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=500, default="", blank=False)
    distrito = models.CharField(max_length=100, default="", blank=False)
    departamento = models.CharField(max_length=100, default="", blank=False)
    codigo_postal = models.CharField(max_length=100, default="", blank=False)
    telefono = models.CharField(max_length=100, default="", blank=False)
    pais = models.CharField(max_length=100, default="", blank=False)
    monto_total = models.IntegerField(default=0)

    estado_pago = models.CharField(max_length=20, choices=EstadoPago.choices, default=EstadoPago.SINPAGAR)

    estado = models.CharField(max_length=50, choices=EstadoPedido.choices, default=EstadoPedido.ENPROCESO)

    modo_pago = models.CharField(max_length=50, choices=ModoPago.choices, default=ModoPago.COD)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    

class ArticuloPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, related_name="articulospedidos")
    nombre = models.CharField(max_length=200, default="", blank=False)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=7, decimal_places=2, blank=False)
    imagen = models.CharField(max_length=500, default="", blank=False)

    def __str__(self):
        return str(self.nombre)