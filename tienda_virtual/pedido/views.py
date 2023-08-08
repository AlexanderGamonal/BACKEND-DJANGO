import os
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *
from .filters import *
from rest_framework.pagination import PageNumberPagination

from .models import *
import stripe
from utils.helpers import get_current_host

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pedidos(request):

    filterset = filtrarPedido(request.GET, queryset=Pedido.objects.all().order_by('id'))

    contador = filterset.qs.count()

    # Paginacion

    resPorPagina = 1
    paginador = PageNumberPagination()
    paginador.page_size = resPorPagina

    queryset = paginador.paginate_queryset(filterset.qs, request)

    serializer = PedidoSerializer(queryset, many=True)

    return Response({
        "contador": contador,
        "resPorPagina": resPorPagina,
        "productos": serializer.data 
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pedido(request, pk):
    pedido = get_object_or_404(Pedido, id=pk)

    serializer = PedidoSerializer(pedido, many=False)

    return Response({ 'pedido': serializer.data })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nuevo_pedido(request):

    user = request.user
    data = request.data

    articulos_pedidos = data['articulosPedidos']

    if articulos_pedidos and len(articulos_pedidos) == 0:
        return Response({ 'error': 'Por favor, añada al menos un producto.' }, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        # crear pedido

        monto_total = sum(articulo['precio']* articulo['cantidad'] for articulo in articulos_pedidos)

        pedido = Pedido.objects.create(
            user = user,
            calle = data['calle'],
            distrito = data['distrito'],
            departamento = data['departamento'],
            codigo_postal = data['codigo_postal'],
            telefono = data['telefono'],
            pais = data['pais'],
            monto_total = monto_total
        )

        # crear artículos de pedido y establecer el orden de los artículos pedidos

        for i in articulos_pedidos:
            producto = Producto.objects.get(id=i['producto'])

            articulo = ArticuloPedido.objects.create(
                producto=producto,
                pedido=pedido,
                nombre=producto.nombre,
                cantidad = i['cantidad'],
                precio= i['precio']
            )

            # Actualizar productos disponibles
            producto.disponible -= articulo.cantidad
            producto.save()

        serializer = PedidoSerializer(pedido, many=False)
        return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def procesar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, id=pk)

    pedido.estado = request.data['estado']

    pedido.save()

    serializer = PedidoSerializer(pedido, many=False)

    return Response({ 'pedido': serializer.data })



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, id=pk)

    pedido.delete()

    return Response({ 'detalles': 'Pedido fue eliminado.' })



stripe.api_key = os.environ.get('STRIPE_PRIVATE_KEY')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    
    YOUR_DOMAIN = get_current_host(request)

    user = request.user
    data = request.data

    articulos_pedidos = data['articulosPedidos']

    shipping_details = {
        'calle': data['calle'],
        'distrito': data['distrito'],
        'departamento': data['departamento'],
        'codigo_postal': data['codigo_postal'],
        'telefono': data['telefono'],
        'pais': data['pais'],
        'user': user.id
    } 

    checkout_articulos_pedidos = []
    for articulo in articulos_pedidos:
        checkout_articulos_pedidos.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    "name": articulo['nombre'],
                    "images": [articulo['imagen']],
                    "metadata": { "product_id": articulo['producto']}
                },
                'unit_amount': articulo['precio'] * 100
            },
            'quantity': articulo['cantidad']
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        metadata = shipping_details,
        line_items=checkout_articulos_pedidos,
        customer_email = user.email,
        mode='payment',
        success_url= YOUR_DOMAIN,
        cancel_url= YOUR_DOMAIN
    )

    return Response({ 'session': session })


@api_view(['POST'])
def stripe_webhook(request):

    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )

    except ValueError as e:
        return Response({ 'error': 'Invalid PayLoad' }, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        return Response({ 'error': 'Invalid Signature' }, status=status.HTTP_400_BAD_REQUEST)
    

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        line_items = stripe.checkout.Session.list_line_items(session['id'])

        precio = session['amount_total'] / 100

        pedido = Pedido.objects.create(
            user = User(session.metadata.user),
            calle = session.metadata.calle,
            distrito = session.metadata.distrito,
            departamento = session.metadata.departamento,
            codigo_postal = session.metadata.codigo_postal,
            telefono = session.metadata.telefono,
            pais = session.metadata.pais,
            monto_total = precio,
            modo_pago = "Card",
            estado_pago = 'PAGADO'
        )

        for articulo in line_items['data']:

            print('articulo', articulo)

            line_product = stripe.Product.retrieve(articulo.price.product)
            product_id = line_product.metadata.product_id

            producto = Producto.objects.get(id=product_id)

            articulo = ArticuloPedido.objects.create(
                producto=producto,
                pedido=pedido,
                nombre= producto.nombre,
                cantidad= articulo.quantity,
                precio= articulo.price.unit_amount / 100,
                imagen= line_product.images[0]
            )

            producto.disponible -= articulo.cantidad
            producto.save()

        
        return Response({ 'detalles': 'Pago realizado' })
