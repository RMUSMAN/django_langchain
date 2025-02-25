from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from ..serializers import LlmRequestSerializer
from utils.utils import validate_api_key 

class OpenAPI(APIView):
    def post(self, request):
       api_key_error = validate_api_key('OPENAPI_API_KEY', 'OpenApi')
       if api_key_error:
           return api_key_error
       
       seriliazer = LlmRequestSerializer(data=request.data)
       seriliazer.is_valid(raise_exception=True)

       question = seriliazer.validated_data['question']

       try:
        llm = OpenAI(
                model="gpt-3.5-turbo",
                openai_api_key=settings.OPENAPI_API_KEY
            )
        prompt = PromptTemplate(
                input_variables=["question"],
                template="Answer this question: {question}"
            )
        chain = prompt | llm
        response = chain.invoke({'question': question})
        
        return Response({
                "question": question,
                "response": response
            })
           
       except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
               


