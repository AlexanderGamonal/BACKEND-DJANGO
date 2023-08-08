from django.urls import path
from . import views

urlpatterns = [
    path('pedidos/nuevo/', views.nuevo_pedido, name='nuevo_pedido'),
    path('pedidos/', views.get_pedidos, name='get_pedidos'),
    path('pedidos/<str:pk>/', views.get_pedido, name='get_pedido'),
    path('pedidos/<str:pk>/procesar/', views.procesar_pedido, name='procesar_pedido'),
    path('pedidos/<str:pk>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),

    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('pedido/webhook/', views.stripe_webhook, name='stripe_webhook')
]