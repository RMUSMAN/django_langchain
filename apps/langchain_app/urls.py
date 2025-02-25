from django.urls import path
from .views.books import BookSearch, BookListCreate
from .views.open_api import OpenAPI
from .views.deepseek import DeepseekView
from .views.ollama import Ollama



urlpatterns = [
    path('books/', BookListCreate.as_view(), name='book-list-create'),
    path('books/search/', BookSearch.as_view(), name='book-search'),
    path('openai/', OpenAPI.as_view(), name='open-ai'),
    path('deepseek-chat/', DeepseekView.as_view(), name='deepseek-ai'),
    path('ollama/', Ollama.as_view(), name='ollama'),



]