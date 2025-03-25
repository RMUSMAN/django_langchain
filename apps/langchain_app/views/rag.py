import os
from rest_framework.response import Response
from langchain_chroma import Chroma
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from ..serializers.prompt_serializer import LLMRequestSerializer
from utils.constants import MODEL_MAPPING
from utils.utils import clean_deepseek_response


persist_dir = os.path.join(settings.BASE_DIR, "chroma_db")
embedding_model = OllamaEmbeddings(model="deepseek-r1:1.5b")


def get_vectorstore():
    if not os.path.exists(persist_dir):
        file_path = os.path.join(settings.BASE_DIR, "utils", "company_data.txt")
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=200,
            length_function=len
        )
        docs = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embedding_model,
            persist_directory=persist_dir
        )
        vectorstore.persist()
    else:
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding_model
        )
    return vectorstore

vectorstore = get_vectorstore()

@api_view(['POST'])
def company_info_chatbot(request):
    serializer = LLMRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    sentence = serializer.validated_data['sentence']
    llm_model_name = serializer.validated_data['llm']  # e.g., "llama3.2"
    llm = OllamaLLM(model=MODEL_MAPPING[llm_model_name])  # Instantiate the LLM
    
    try:
        results = vectorstore.similarity_search(sentence, k=4)
        if results:
            context = " ".join([doc.page_content for doc in results])
            response = llm.invoke(f"Answer this: {sentence}. Context: {context}")
        else:
            response = llm.invoke(f"Answer the question: {sentence}, even if no relevant context is available.")

        return Response({
            "question": sentence,
            "response": clean_deepseek_response(response)
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )