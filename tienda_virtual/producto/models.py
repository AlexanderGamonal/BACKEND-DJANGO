from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Create your models here.

class Categoria(models.TextChoices):
    COMPUTADORAS = 'Computadoras'
    LAPTOPS = 'Laptops'
    CELULARES = 'Celulares'
    TABLETS = 'Tablets'

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre =  models.CharField('Nombre', max_length=100, default="", blank=True)
    descripcion = models.TextField(max_length=200, blank=False)
    precio = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    marca = models.CharField(max_length=200, default="", blank=False)
    categoria = models.CharField(max_length=30, choices=Categoria.choices)
    valoraciones = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    disponible = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class ProductoImagenes(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, related_name="imagenes")
    imagen = models.ImageField(upload_to="productos")


@receiver(post_delete, sender=ProductoImagenes)
def auto_delete_file_delete(sender, instance, **kwargs):
    if instance.imagen:
        instance.imagen.delete(save=False)


class Review(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    valoracion = models.IntegerField(default=0)
    comentario = models.TextField(default="", blank=False)
    fechaCreacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comentario)
