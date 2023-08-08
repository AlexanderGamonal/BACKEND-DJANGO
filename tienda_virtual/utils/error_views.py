from django.http import JsonResponse


def handler404(request, exception):
    mensaje = ('Ruta no funciona')
    response = JsonResponse(data={'error': mensaje})
    response.status_code = 404
    return response


def handler500(request):
    mensaje = ('Error interno del servidor')
    response = JsonResponse(data={'error': mensaje})
    response.status_code = 500
    return response




