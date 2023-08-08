from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Avg

from .filters import ProductosFilter

from .serializers import ProductoSerializer, ProductoImagenesSerializer

from .models import Producto, ProductoImagenes, Review

# Create your views here.

@api_view(['GET'])
def get_productos(request):

    filterset = ProductosFilter(request.GET, queryset=Producto.objects.all().order_by('id'))

    contador = filterset.qs.count()

    # Paginacion
    resPorPagina= 5

    paginador = PageNumberPagination()

    paginador.page_size = resPorPagina

    queryset = paginador.paginate_queryset(filterset.qs, request)

    serializer = ProductoSerializer(queryset, many=True)

    return Response({
        "contador": contador,
        "resPorPagina": resPorPagina,
        "productos": serializer.data 
        })


@api_view(['GET'])
def get_producto(request, pk):

    producto = get_object_or_404(Producto, id=pk)

    serializer = ProductoSerializer(producto, many=False)

    return Response({ "producto": serializer.data })



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def nuevo_producto(request):

    data = request.data

    serializer = ProductoSerializer(data=data)

    if serializer.is_valid():

        producto = Producto.objects.create(**data, user=request.user)

        res = ProductoSerializer(producto, many=False)

        return Response({ "producto": res.data })
    
    else:
        return Response(serializer.errors)



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def upload_producto_imagenes(request):

    data = request.data

    files = request.FILES.getlist('imagenes')

    imagenes = []
    for i in files:
        imagen = ProductoImagenes.objects.create(producto=Producto(data['producto']), imagen=i)
        imagenes.append(imagen)

    serializer = ProductoImagenesSerializer(imagenes, many=True)    

    return Response( serializer.data )



@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, id=pk)

    if producto.user != request.user:
        return Response({ 'error': 'Solo el usuario que lo creo puede actualizar este producto' }, status=status.HTTP_403_FORBIDDEN)

    producto.nombre = request.data['nombre']
    producto.descripcion = request.data['descripcion']
    producto.precio = request.data['precio']
    producto.categoria = request.data['categoria']
    producto.marca = request.data['marca']
    producto.valoraciones = request.data['valoraciones']
    producto.disponible = request.data['disponible']

    producto.save()

    serializer = ProductoSerializer(producto, many=False)

    return Response({ "producto": serializer.data })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, id=pk)

    if producto.user != request.user:
        return Response({ 'error': 'Solo el usuario que lo creo puede eliminar este producto' }, status=status.HTTP_403_FORBIDDEN)

    args = { "producto": pk }
    imagenes = ProductoImagenes.objects.filter(**args)

    for i in imagenes:
        i.delete()

    producto.delete()

    return Response({ "detalles": "producto eliminado" }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def crear_review(request, pk):
    user = request.user
    producto = get_object_or_404(Producto, id=pk)
    data = request.data

    review = producto.reviews.filter(user=user)

    if data['valoracion'] <= 0 or data['valoracion'] > 5:
        return Response({'message':'Seleccione una Valoración entre 1-5 por favor'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif review.exists():

        new_review = { 'valoracion': data['valoracion'], 'comentario': data['comentario'] }
        review.update(**new_review)

        valoracion = producto.reviews.aggregate(avg_valoraciones=Avg('valoracion'))

        producto.valoraciones = valoracion['avg_valoraciones']

        producto.save()

        return Response({ 'detalle': 'Revision actualizada' })
    
    else:
        Review.objects.create(
            user = user,
            producto = producto,
            valoracion = data['valoracion'],
            comentario = data['comentario']
        )

        valoracion = producto.reviews.aggregate(avg_valoraciones=Avg('valoracion'))

        producto.valoraciones = valoracion['avg_valoraciones']

        producto.save()

        return Response({ 'detalle': 'Revision publicada' })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_review(request, pk):
    user = request.user
    producto = get_object_or_404(Producto, id=pk)

    review = producto.reviews.filter(user=user)

    if review.exists():

        review.delete()

        valoracion = producto.reviews.aggregate(avg_valoraciones=Avg('valoracion'))

        if valoracion['avg_valoraciones'] is None:
            valoracion['avg_valoraciones'] = 0

        producto.valoraciones = valoracion['avg_valoraciones']
        producto.save()

        return Response({ 'detalle': 'Revision eliminada' })

    else:
        return Response({ 'error': 'Revision no encontrada' })