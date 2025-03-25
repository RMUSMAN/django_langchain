from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from langchain_core.prompts import ChatPromptTemplate
from ..serializers.prompt_serializer import LLMRequestSerializer
from langchain_ollama.llms import OllamaLLM
from utils.constants import MODEL_MAPPING
from langchain_core.output_parsers import StrOutputParser

class LanguageTranslator(APIView):
    def post(self, request):

       seriliazer = LLMRequestSerializer(data=request.data)
       seriliazer.is_valid(raise_exception=True)

       sentence = seriliazer.validated_data['sentence']
       convert_to_language = seriliazer.validated_data['convert_to_language']
       llm = seriliazer.validated_data['llm']
       
       try:
        prompt = ChatPromptTemplate([
           "system", """You are a professional translator. Follow these rules:
1. Translate directly without explanations
2. Preserve numbers, names, and technical terms
3. Maintain original formatting
4. Respond ONLY with the translation""",
           "human", "Translate this to {convert_to_language}:\n{sentence}"
        ])
        model = OllamaLLM(model=MODEL_MAPPING[llm])
        chain = prompt | model | StrOutputParser()
        response = chain.invoke({'sentence': sentence, 'convert_to_language': convert_to_language})

        return Response({
                "sentence": sentence,
                "response": response
            })
           
       except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
               


