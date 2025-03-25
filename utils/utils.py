import re
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from langchain_core.output_parsers import StrOutputParser


from langchain_ollama.llms import OllamaLLM
from utils.constants import MODEL_MAPPING

def validate_api_key(api_key_setting, service_name):
    if not getattr(settings, api_key_setting, None):
        return Response(
            {"error": f"{service_name} API key not configured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return None


def run_Ollama_llm(llm, prompt, input_text_data):
     model = OllamaLLM(model=MODEL_MAPPING[llm])
     chain = prompt | model | StrOutputParser()
     response = chain.invoke(input_text_data)     
     return Response({
                "user_input": input_text_data,
                "response": response.strip().replace("\n", " ")
            })

def clean_deepseek_response(response):
    cleaned = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    return cleaned