from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..models.book import Book
from ..serializers.serializers import BookSerializer


class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookSearch(APIView):
    def get(self, request):
        author = request.query_params.get('author')
        if author:
            books = Book.objects.filter(author__icontains=author)
            serializer  = BookSerializer(books, many=True)
            return Response(serializer.data)
        return Response({'error': 'Please provide author name'}, status=status.HTTP_400_BAD_REQUEST)
