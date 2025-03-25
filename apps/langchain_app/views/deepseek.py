from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_core.prompts import PromptTemplate
from django.conf import settings
from langchain_deepseek import ChatDeepSeek
from ..serializers.serializers import LlmRequestSerializer
from utils.utils import validate_api_key 

class DeepseekView(APIView):
    def post(self, request):
        api_key_error = validate_api_key('DEEPSEEK_API_KEY', 'DeepSeek')
        if api_key_error:
            return api_key_error
        
        serializer = LlmRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        question = serializer.validated_data['question']
        temperature = serializer.validated_data["temperature"]
        print(question, temperature)

        try:
           
        
            llm = ChatDeepSeek(
                temperature=temperature,
                api_key=settings.DEEPSEEK_API_KEY,
                model="deepseek-chat",
                max_tokens=None,
                timeout=None,
            )

            prompt = PromptTemplate(
                input_variables=["question"],
                template="""You are a helpful AI assistant. Answer this question in detail:
                
                Question: {question}
                Answer:"""
            )
            
            chain = prompt | llm
            response = chain.invoke({'question':question})
            
            return Response({
                "question": question,
                "response": response,
                "model": "deepseek-chat"
            })
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    