import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.ticket import SupportTicket
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.utils import clean_deepseek_response

embedding_model = OllamaEmbeddings(model="nomic-embed-text")
llm = OllamaLLM(model="gemma2:2b")
persist_dir = os.path.join(settings.BASE_DIR, "chroma_db")

def initialize_vectorstore():
    if not os.path.exists(persist_dir):
        tickets = SupportTicket.objects.all()
        documents = [
            Document(
                page_content=f"Issue: {ticket.issue_description}\nResolution: {ticket.resolution}",
                metadata={"ticket_id": ticket.ticket_id, "customer_name": ticket.customer_name}
            )
            for ticket in tickets
        ]
 
        vectorstore = Chroma.from_documents(
            documents=documents,
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

vectorstore = initialize_vectorstore()

@api_view(['POST'])
def support_chatbot(request):
    try:
        query = request.data.get('query', '')
        if not query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve relevant tickets
        results = vectorstore.similarity_search(query, k=4)
        context = "\n\n".join([doc.page_content for doc in results])
    
        prompt = (
            f"Provide a answer to the question '{query}' based on the following context. "
            f"Do not include extra information:\n\n{context}"
        )
        response = llm.invoke(prompt)

        return Response({
            "query": query,
            "response": clean_deepseek_response(response),
            "source_tickets": [doc.metadata["ticket_id"] for doc in results]
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)