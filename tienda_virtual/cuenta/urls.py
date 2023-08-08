from django.urls import path
from . import views


urlpatterns = [
    path('registro/', views.registro, name="registro"),
    path('mi/', views.current_user, name="current_user"),
    path('mi/actualizar/', views.actualizar_usuario, name="actualizar_usuario"),
    path('olvide_password/', views.olvide_password, name="olvide_password"),
    path('reset_password/<str:token>', views.reset_password, name="reset_password")
]