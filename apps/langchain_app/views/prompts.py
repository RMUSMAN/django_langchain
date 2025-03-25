from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from langchain_core.prompts import PromptTemplate

from utils.utils import run_Ollama_llm
from ..serializers.prompt_serializer import LLMRequestSerializer


@api_view(['POST'])
def zero_shot_prompt(request):
    
    seriliazer = LLMRequestSerializer(data=request.data)
    seriliazer.is_valid(raise_exception=True)
    sentence = seriliazer.validated_data['sentence']
    llm = seriliazer.validated_data['llm']

    try:
        prompt_template = PromptTemplate(
        input_variables=["sentence"],
        template=f"Classify the sentiment of texts as positive, negative, or neutral: {sentence}"
        )
        return run_Ollama_llm(llm, prompt_template,{'sentence': sentence})

    except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   
   
@api_view(['POST'])
def few_shot_prompt(request):
    
    FEW_SHOT_EXAMPLES = """
You are an assistant that helps with text processing. Here are some examples:

User: Summarize: "Django is a high-level Python web framework."
AI: Django is a Python web framework for rapid development.

User: Translate to French: "Hello, how are you?"
AI: Bonjour, comment ça va?

User: Complete the sentence: "The sun is..."
AI: The sun is a massive ball of gas that provides light and heat.
"""
    seriliazer = LLMRequestSerializer(data=request.data)
    seriliazer.is_valid(raise_exception=True)
    sentence = seriliazer.validated_data['sentence']
    llm = seriliazer.validated_data['llm']

    try:
        prompt_template = PromptTemplate(
        input_variables=["sentence"],
        template=f"{FEW_SHOT_EXAMPLES}\nUser: {sentence}\nAI:"
        )
        return run_Ollama_llm(llm, prompt_template,{'sentence': sentence})

    except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   
   
@api_view(['POST'])
def cot_shot_prompt(request):
   
    seriliazer = LLMRequestSerializer(data=request.data)
    seriliazer.is_valid(raise_exception=True)
    sentence = seriliazer.validated_data['sentence']
    llm = seriliazer.validated_data['llm']
    CoT_PROMPT = """
You are a math tutor who solves problems step by step. Follow the Chain of Thought (CoT) approach to provide detailed reasoning.

Example 1:
Question: If a train travels 60 km in 1 hour, how far does it travel in 3 hours?
Step 1: The speed of the train is 60 km per hour.
Step 2: In 3 hours, the distance traveled is 60 * 3.
Answer: 180 km.

Example 2:
Question: John has 5 apples. He buys 3 more and gives away 2. How many does he have?
Step 1: John starts with 5 apples.
Step 2: He buys 3 more, so now he has 5 + 3 = 8.
Step 3: He gives away 2, so now he has 8 - 2.
Answer: 6 apples.

Now, solve this question step by step:
Question: {sentence}
"""

    try:
        prompt_template = PromptTemplate(
        input_variables=["sentence"],
        template=CoT_PROMPT
        )
        return run_Ollama_llm(llm, prompt_template,{'sentence': sentence})

    except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   
@api_view(['POST'])
def role_based_agent(request):
   
    seriliazer = LLMRequestSerializer(data=request.data)
    seriliazer.is_valid(raise_exception=True)
    sentence = seriliazer.validated_data['sentence']
    llm = seriliazer.validated_data['llm']
    role = seriliazer.validated_data['role']

    CoT_PROMPT = """
You are a highly intelligent assistant that provides step-by-step explanations. Your role is: {role}

Example 1 (Math Tutor):
User: If a car travels 60 km per hour, how far does it go in 3 hours?
AI (Math Tutor): 
Step 1: The car moves at 60 km/h.
Step 2: In 3 hours, distance = 60 * 3.
Answer: 180 km.

Example 2 (Doctor):
User: I have a headache and fever, what could it be?
AI (Doctor):
Step 1: Headache and fever are common symptoms.
Step 2: Possible causes: flu, dehydration, migraine.
Step 3: If symptoms persist, consult a physician.
Answer: Possible flu or dehydration. Drink water and rest.

Example 3 (Lawyer):
User: Can I get a refund if a store refuses?
AI (Lawyer):
Step 1: Refund policies depend on the store.
Step 2: If faulty product, consumer law protects you.
Step 3: If store policy allows, you can return.
Answer: Check store policy; consumer law may apply.

Now, act as {role} and answer the question:
User: {sentence}
"""

  
    try:
        prompt_template = PromptTemplate(
        input_variables=["sentence"],
        template=CoT_PROMPT
        )
        return run_Ollama_llm(llm, prompt_template,{'sentence': sentence, 'role': role})

    except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   
   