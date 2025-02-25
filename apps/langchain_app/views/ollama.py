from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from langchain_core.prompts import PromptTemplate
from ..serializers import LlmRequestSerializer
from langchain_ollama.llms import OllamaLLM
from utils.constants import MODEL_MAPPING

class Ollama(APIView):
    def post(self, request):

       seriliazer = LlmRequestSerializer(data=request.data)
       seriliazer.is_valid(raise_exception=True)

       question = seriliazer.validated_data['question']
       llm = seriliazer.validated_data['llm']
       try:

        prompt = PromptTemplate(
                input_variables=["question"],
                template="Answer this question: {question}"
            )
        model = OllamaLLM(model=MODEL_MAPPING[llm])
        chain = prompt | model
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
               


