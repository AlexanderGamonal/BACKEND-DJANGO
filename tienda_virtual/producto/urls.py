from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.get_productos, name='productos'),
    path('productos/nuevo/', views.nuevo_producto, name='nuevo_producto'),
    path('productos/upload_imagenes/', views.upload_producto_imagenes, name="upload_producto_imagenes"),
    path('productos/<str:pk>/', views.get_producto, name="get_producto_detalle"),
    path('productos/<str:pk>/actualizar/', views.actualizar_producto, name="actualizar_producto"),
    path('productos/<str:pk>/eliminar/', views.eliminar_producto, name="eliminar_producto"),

    path('<str:pk>/reviews/', views.crear_review, name="crear_actualizar_review"),
    path('<str:pk>/reviews/eliminar/', views.eliminar_review, name="eliminar_review")
]

