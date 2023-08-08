from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from http import HTTPStatus

def custom_exception_handler(exc, context):
    
    response = exception_handler(exc, context)
    
    if response is not None:
        
        http_code_mensaje = { v.value: v.description for v in HTTPStatus }

        error_payload = {
            'error': {
                'status_code': 0,
                'mensaje': "",
                'detalles': []
            }
        }

        error = error_payload["error"]
        status_code = response.status_code

        error["status_code"] = status_code
        error["mensaje"] = http_code_mensaje[status_code]
        error["detalles"] = response.data

        response.data = error_payload

        return response
    
    

