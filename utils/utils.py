from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

def validate_api_key(api_key_setting, service_name):
    if not getattr(settings, api_key_setting, None):
        return Response(
            {"error": f"{service_name} API key not configured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return None