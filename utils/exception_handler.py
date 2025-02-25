from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If response is already handled by DRF, return it
    if response is not None:
        return response
    
    error_response = {
        'error': True,
        'message': str(exc)
    }
    
    # Handle different types of exceptions
    if isinstance(exc, ValidationError):
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exc, IntegrityError):
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
    elif isinstance(exc, KeyError):
        error_response['message'] = f"Missing required parameter: {str(exc)}"
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    
    # Add any other custom exceptions you'd like to handle
    
    # If no specific handler, return generic 500 error
    return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)