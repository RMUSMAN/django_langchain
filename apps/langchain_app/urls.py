from django.urls import path
from .views.books import BookSearch, BookListCreate
from .views.open_api import OpenAPI
from .views.deepseek import DeepseekView
from .views.ollama import Ollama
from .views.language_translator import LanguageTranslator
from .views.prompts import few_shot_prompt, zero_shot_prompt,cot_shot_prompt, role_based_agent
from .views.rag import company_info_chatbot


urlpatterns = [
    path('books/', BookListCreate.as_view(), name='book-list-create'),
    path('books/search/', BookSearch.as_view(), name='book-search'),
    path('openai/', OpenAPI.as_view(), name='open-ai'),
    path('deepseek-chat/', DeepseekView.as_view(), name='deepseek-ai'),
    path('ollama/', Ollama.as_view(), name='ollama'),
    path('language-translator/', LanguageTranslator.as_view(), name='language-translator'),
    path('zero_shot_prompt/', zero_shot_prompt, name='zero-shot-prompt'),
    path('few_shot_prompt/', few_shot_prompt, name='few-shot-prompt'),
    path('cot_prompt_math_tutor/', cot_shot_prompt, name='cot-shot-prompt'),
    path('role_based_agent/', role_based_agent, name='role-based-agent'),
    path('company_info_chatbot/', company_info_chatbot, name='company-info-chatbot'),


]