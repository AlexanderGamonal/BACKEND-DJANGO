from dataclasses import field
from rest_framework import serializers
from .models import *


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class ProductoImagenesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductoImagenes
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):

    imagenes = ProductoImagenesSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(method_name="get_reviews", read_only=True)

    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'precio', 'marca', 'categoria', 'valoraciones', 'disponible', 'user', 'reviews', 'imagenes')

        extra_kwargs = {
            "nombre": { "required": True, "allow_blank": False },
            "descripcion": { "required": True, "allow_blank": False },
            "marca": { "required": True, "allow_blank": False },
            "categoria": { "required": True, "allow_blank": False }
        }

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
        

